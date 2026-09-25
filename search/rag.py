import re
import time
import json
import hashlib

from django.conf import settings
from django.core.cache import cache

from products.models import Product

from .hybrid import hybrid_search, tokenize


MAX_QUERY_CHARS = getattr(settings, "MAX_QUERY_CHARS", 500)
K_CONTEXT = getattr(settings, "SEARCH_RAG_CONTEXT_SIZE", 8)
MAX_RECOMMENDED = 4
CACHE_TTL = 300

INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions?", re.I),
    re.compile(r"disregard\s+(?:all\s+)?(?:previous|prior)\s+(?:instructions?|prompts?|messages?)", re.I),
    re.compile(r"system\s*[:|]", re.I),
    re.compile(r"you\s+are\s+now\s+", re.I),
    re.compile(r"forget\s+(?:everything|all|previous)", re.I),
    re.compile(r"</?(?:user_query|system|context|instructions?)>", re.I),
]


def sanitize_query(text):
    original = text or ""
    q = original.strip()
    truncated = False
    if len(q) > MAX_QUERY_CHARS:
        q = q[:MAX_QUERY_CHARS]
        truncated = True
    injection = False
    for pattern in INJECTION_PATTERNS:
        if pattern.search(q):
            injection = True
            q = pattern.sub("[...]", q)
    q = re.sub(r"\s+", " ", q).strip()
    return {"query": q, "truncated": truncated, "injection": injection, "original": original}


def _match_reasons(product, query_tokens):
    haystack = set(tokenize(product.title))
    for tag in product.tag_set.all():
        haystack |= set(tokenize(tag.title))
    if product.category_id and product.category:
        haystack |= set(tokenize(product.category.name))
    seen = []
    for token in query_tokens:
        if token in haystack and token not in seen:
            seen.append(token)
    return seen[:4]


def _explain(product, query_tokens):
    reasons = _match_reasons(product, query_tokens)
    if reasons:
        return "Matches: " + ", ".join(reasons)
    category = product.category.name if product.category_id and product.category else None
    if category:
        return "{category}{grammage}".format(
            category=category,
            grammage=", {g}".format(g=product.grammage) if product.grammage else "",
        )
    return ""


def _summary(query, products):
    if not products:
        return "No matching product found. Try another word, or browse the categories."
    top = products[0]
    categories = []
    for product in products:
        if product.category_id and product.category and product.category.name not in categories:
            categories.append(product.category.name)
    lead = '{n} pick{s} for "{q}".'.format(n=len(products), s="" if len(products) == 1 else "s", q=query)
    detail = " Top choice: {title} at {price} EUR.".format(title=top.title, price=top.price)
    if categories:
        detail += " From " + ", ".join(categories[:3]) + "."
    return lead + detail


def _cache_key(query):
    payload = json.dumps({"q": query.strip().lower()}, ensure_ascii=False)
    return "rag:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ask(query, k_context=K_CONTEXT):
    started = time.time()
    sanitized = sanitize_query(query)
    if not sanitized["query"]:
        return {
            "query": query,
            "summary": "What are you looking for? For example a gift, something spicy, or a specific product.",
            "products": [],
            "clarifying_question": None,
            "clarifying_options": [],
            "insufficient_data": True,
            "diagnostics": {"mode": "local", "cached": False, "latency_ms": 0, "retrieved_count": 0},
        }

    key = _cache_key(sanitized["query"])
    cached = cache.get(key)
    if cached:
        products_by_id = Product.objects.in_bulk([spec["id"] for spec in cached["product_specs"]])
        products = [
            {"product": products_by_id[spec["id"]], "explanation": spec["explanation"]}
            for spec in cached["product_specs"] if spec["id"] in products_by_id
        ]
        diagnostics = dict(cached["diagnostics"])
        diagnostics["cached"] = True
        diagnostics["latency_ms"] = int((time.time() - started) * 1000)
        return {
            "query": query,
            "summary": cached["summary"],
            "products": products,
            "clarifying_question": None,
            "clarifying_options": [],
            "insufficient_data": cached["insufficient_data"],
            "diagnostics": diagnostics,
        }

    retrieved = hybrid_search(sanitized["query"], k_final=k_context)
    picks = retrieved[:MAX_RECOMMENDED]
    query_tokens = tokenize(sanitized["query"])
    products = [{"product": product, "explanation": _explain(product, query_tokens)} for product in picks]

    insufficient = len(products) == 0
    summary = _summary(sanitized["query"], picks)
    diagnostics = {
        "mode": "local",
        "cached": False,
        "latency_ms": int((time.time() - started) * 1000),
        "retrieved_count": len(retrieved),
    }
    result = {
        "query": query,
        "summary": summary,
        "products": products,
        "clarifying_question": None,
        "clarifying_options": [],
        "insufficient_data": insufficient,
        "diagnostics": diagnostics,
    }

    cache.set(key, {
        "summary": summary,
        "product_specs": [{"id": item["product"].id, "explanation": item["explanation"]} for item in products],
        "insufficient_data": insufficient,
        "diagnostics": diagnostics,
    }, CACHE_TTL)

    return result
