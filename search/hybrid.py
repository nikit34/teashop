import re
import functools
import unicodedata

from django.conf import settings

from products.models import Product


RRF_K = 60
TOP_K_BM25 = 30
TOP_K_DENSE = 30
TOP_K_FINAL = 12
DENSE_MIN_SCORE = getattr(settings, "SEARCH_DENSE_MIN_SCORE", 0.3)
EMBEDDING_MODEL = getattr(settings, "SEARCH_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

_TOKEN_RE = re.compile(r"[^\W\d_]+|\d+", re.UNICODE)


def fold_accents(text):
    decomposed = unicodedata.normalize("NFKD", text or "")
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def tokenize(text):
    return [t.lower() for t in _TOKEN_RE.findall(fold_accents(text))]


def product_document(product):
    parts = [product.title or "", product.description or ""]
    if product.category_id and product.category:
        parts.append(product.category.name)
    parts.extend(tag.title for tag in product.tag_set.all())
    return " ".join(parts)


def _active_products():
    return list(
        Product.objects.all().select_related("category").prefetch_related("tag_set")
    )


def _bm25_rank(products, query, top_k):
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        return _fallback_rank(products, query, top_k)

    corpus = [tokenize(product_document(p)) for p in products]
    if not any(corpus):
        return []
    tokens = tokenize(query)
    if not tokens:
        return []
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(tokens)
    query_tokens = set(tokens)
    ranked = sorted(
        ((products[i], scores[i]) for i in range(len(products)) if query_tokens & set(corpus[i])),
        key=lambda pair: pair[1],
        reverse=True,
    )
    return ranked[:top_k]


def _fallback_rank(products, query, top_k):
    q = (query or "").lower()
    hits = []
    for p in products:
        haystack = product_document(p).lower()
        if q and q in haystack:
            hits.append((p, float(haystack.count(q))))
    hits.sort(key=lambda pair: pair[1], reverse=True)
    return hits[:top_k]


@functools.lru_cache(maxsize=1)
def _embedder():
    try:
        from fastembed import TextEmbedding
    except ImportError:
        return None
    try:
        return TextEmbedding(model_name=EMBEDDING_MODEL)
    except Exception:
        return None


def _needs_e5_prefix():
    return "e5" in EMBEDDING_MODEL.lower()


def embed_passages(texts):
    model = _embedder()
    if model is None:
        return None
    if _needs_e5_prefix():
        texts = ["passage: {text}".format(text=t) for t in texts]
    return [vec.tolist() for vec in model.embed(list(texts))]


def _embed_query(query):
    model = _embedder()
    if model is None:
        return None
    if _needs_e5_prefix():
        query = "query: {query}".format(query=query)
    for vec in model.embed([query]):
        return vec
    return None


def _dense_rank(products, query, top_k):
    try:
        import numpy as np
    except ImportError:
        return []
    from .models import ProductEmbedding

    stored = {
        pe.product_id: pe.vector
        for pe in ProductEmbedding.objects.filter(product__in=products)
    }
    if not stored:
        return []
    qvec = _embed_query(query)
    if qvec is None:
        return []

    q = np.asarray(qvec, dtype="float32")
    q_norm = np.linalg.norm(q)
    if q_norm == 0:
        return []
    q = q / q_norm

    scored = []
    for product in products:
        vector = stored.get(product.id)
        if not vector:
            continue
        v = np.asarray(vector, dtype="float32")
        v_norm = np.linalg.norm(v)
        if v_norm == 0:
            continue
        score = float(q @ (v / v_norm))
        if score >= DENSE_MIN_SCORE:
            scored.append((product, score))
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]


def _rrf_merge(bm25_results, dense_results, k_final):
    merged = {}
    for rank, (product, score) in enumerate(bm25_results, start=1):
        merged[product.id] = {
            "product": product,
            "score": 1.0 / (RRF_K + rank),
        }
    for rank, (product, score) in enumerate(dense_results, start=1):
        entry = merged.get(product.id)
        if entry:
            entry["score"] += 1.0 / (RRF_K + rank)
        else:
            merged[product.id] = {
                "product": product,
                "score": 1.0 / (RRF_K + rank),
            }
    ordered = sorted(merged.values(), key=lambda entry: entry["score"], reverse=True)
    return [entry["product"] for entry in ordered[:k_final]]


def _pin_exact(products, query, ranked, k_final):
    q = fold_accents((query or "").strip().lower())
    if not q:
        return ranked[:k_final]
    pinned = [p for p in products if q in fold_accents((p.title or "").lower())]
    if not pinned:
        return ranked[:k_final]
    seen = set()
    out = []
    for product in pinned + ranked:
        if product.id in seen:
            continue
        seen.add(product.id)
        out.append(product)
    return out[:k_final]


def hybrid_search(query, k_final=TOP_K_FINAL):
    products = _active_products()
    if not products:
        return []
    if not (query or "").strip():
        featured = [p for p in products if p.featured]
        return featured or products[:k_final]

    bm25_results = _bm25_rank(products, query, TOP_K_BM25)
    dense_results = _dense_rank(products, query, TOP_K_DENSE)
    if not bm25_results and not dense_results:
        return [product for product, _ in _fallback_rank(products, query, k_final)]
    ranked = _rrf_merge(bm25_results, dense_results, max(k_final * 2, k_final + 10))
    return _pin_exact(products, query, ranked, k_final)
