from django.core.management.base import BaseCommand

from products.models import Product
from search.hybrid import EMBEDDING_MODEL, embed_passages, product_document
from search.models import ProductEmbedding


class Command(BaseCommand):
    help = "Compute and store dense embeddings for active products (hybrid search index)"

    def add_arguments(self, parser):
        parser.add_argument("--rebuild", action="store_true", help="Recompute all embeddings, ignoring existing ones")

    def handle(self, *args, **options):
        products = list(Product.objects.all().select_related("category").prefetch_related("tag_set"))
        if not products:
            self.stdout.write("No active products to index")
            return

        if not options["rebuild"]:
            indexed = set(ProductEmbedding.objects.values_list("product_id", flat=True))
            products = [p for p in products if p.id not in indexed]
            if not products:
                self.stdout.write("Index already up to date")
                return

        documents = [product_document(p) for p in products]
        vectors = embed_passages(documents)
        if vectors is None:
            self.stderr.write(
                "fastembed is not installed, dense index skipped. "
                "Search still runs on BM25. Install fastembed to enable semantic search."
            )
            return

        count = 0
        for product, vector in zip(products, vectors):
            ProductEmbedding.objects.update_or_create(
                product=product,
                defaults={
                    "vector": vector,
                    "model_name": EMBEDDING_MODEL,
                    "dim": len(vector),
                },
            )
            count += 1

        self.stdout.write(self.style.SUCCESS("Indexed {count} products with {model}".format(count=count, model=EMBEDDING_MODEL)))
