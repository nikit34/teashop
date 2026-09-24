from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Category, Product
from tags.models import Tag


CATEGORIES = [
    ("Conservas", 10),
    ("Azeite & Vinagre", 20),
    ("Cafe", 30),
    ("Cha dos Acores", 40),
    ("Mel & Docaria", 50),
    ("Sal & Especiarias", 60),
    ("Cabazes", 70),
]


CATALOG = [
    {
        "title": "Sardinhas em Azeite Extra Virgem - Sardines in Extra Virgin Olive Oil",
        "category": "Conservas",
        "price": "6.50",
        "grammage": "120g",
        "featured": True,
        "tags": ["conserva", "sardinha", "azeite", "sem gluten", "artesanal"],
        "description": "Whole sardines hand-packed in extra virgin olive oil, in the northern canning tradition of Matosinhos. Rich, meaty and ready to serve on toasted bread.",
    },
    {
        "title": "Cavala em Azeite - Mackerel Fillets in Olive Oil",
        "category": "Conservas",
        "price": "5.20",
        "grammage": "120g",
        "tags": ["conserva", "cavala", "azeite", "sem gluten"],
        "description": "Tender mackerel fillets in olive oil. A leaner, more affordable everyday tin with the same Atlantic character as sardine.",
    },
    {
        "title": "Atum dos Acores em Azeite - Azores Tuna in Olive Oil",
        "category": "Conservas",
        "price": "7.90",
        "grammage": "120g",
        "featured": True,
        "tags": ["conserva", "atum", "acores", "azeite", "pesca sustentavel"],
        "description": "Pole-and-line skipjack tuna from the Azores, packed in olive oil. Sustainably caught, firm texture, a step above supermarket tuna.",
    },
    {
        "title": "Filetes de Sardinha Picante - Spicy Sardine Fillets",
        "category": "Conservas",
        "price": "5.80",
        "grammage": "120g",
        "tags": ["conserva", "sardinha", "picante", "piri-piri"],
        "description": "Boneless sardine fillets with piri-piri. For anyone who likes a bit of heat with their aperitivo.",
    },
    {
        "title": "Polvo em Azeite - Octopus in Olive Oil",
        "category": "Conservas",
        "price": "9.50",
        "grammage": "120g",
        "tags": ["conserva", "polvo", "azeite", "gourmet"],
        "description": "Cooked octopus in olive oil, a Portuguese delicacy in a tin. Serve cold with a squeeze of lemon or warm over potatoes.",
    },
    {
        "title": "Berbigao ao Natural - Cockles in Brine",
        "category": "Conservas",
        "price": "6.90",
        "grammage": "110g",
        "tags": ["conserva", "berbigao", "marisco"],
        "description": "Ria de Aveiro cockles packed in brine. The base of a quick arroz de marisco or a briny snack straight from the tin.",
    },
    {
        "title": "Pate de Sardinha - Sardine Pate",
        "category": "Conservas",
        "price": "3.90",
        "grammage": "75g",
        "tags": ["conserva", "sardinha", "pate", "petisco"],
        "description": "Smooth sardine pate to spread on bread or crackers. The easiest way to bring tinned fish to a table of guests.",
    },
    {
        "title": "Azeite Virgem Extra DOP Tras-os-Montes",
        "category": "Azeite & Vinagre",
        "price": "12.90",
        "grammage": "500ml",
        "featured": True,
        "tags": ["azeite", "dop", "tras-os-montes", "bio", "presente"],
        "description": "Protected-origin (DOP) extra virgin olive oil from Tras-os-Montes, cold pressed. Intense, peppery finish for finishing dishes rather than frying.",
    },
    {
        "title": "Azeite Virgem Extra do Alentejo",
        "category": "Azeite & Vinagre",
        "price": "14.50",
        "grammage": "750ml",
        "tags": ["azeite", "alentejo", "gourmet"],
        "description": "Everyday-to-premium Alentejo extra virgin olive oil. Balanced and fruity, the workhorse bottle for a Portuguese kitchen.",
    },
    {
        "title": "Azeite Biologico - Organic Extra Virgin Olive Oil",
        "category": "Azeite & Vinagre",
        "price": "13.90",
        "grammage": "500ml",
        "tags": ["azeite", "bio", "organico", "vegan"],
        "description": "Certified organic extra virgin olive oil from Portuguese groves. For buyers who read the label before they buy.",
    },
    {
        "title": "Vinagre de Vinho do Porto - Port Wine Vinegar",
        "category": "Azeite & Vinagre",
        "price": "8.50",
        "grammage": "250ml",
        "tags": ["vinagre", "porto", "gourmet", "presente"],
        "description": "Vinegar aged from Port wine, deep and slightly sweet. A few drops lift salads, sauces and roasted vegetables.",
    },
    {
        "title": "Cafe Torrado em Grao - Whole Bean Roast",
        "category": "Cafe",
        "price": "7.50",
        "grammage": "250g",
        "tags": ["cafe", "grao", "torra"],
        "description": "Classic Portuguese dark roast in whole bean. Chocolatey and low-acid, built for espresso and bica.",
    },
    {
        "title": "Cafe Moido Lote Bica - Ground Espresso Blend",
        "category": "Cafe",
        "price": "6.90",
        "grammage": "250g",
        "tags": ["cafe", "moido", "espresso", "bica"],
        "description": "Ready-ground blend for the classic bica. Arabica and robusta balanced for crema and body.",
    },
    {
        "title": "Cafe de Especialidade Microlote - Specialty Single-Origin",
        "category": "Cafe",
        "price": "11.90",
        "grammage": "250g",
        "featured": True,
        "tags": ["cafe", "especialidade", "microlote", "gourmet"],
        "description": "A single-origin specialty micro-lot roasted for filter and pour-over. Bright and floral, aimed at the third-wave coffee crowd in Lisbon and Porto.",
    },
    {
        "title": "Capsulas Compostaveis - Compostable Coffee Capsules x10",
        "category": "Cafe",
        "price": "4.50",
        "grammage": "10 un",
        "tags": ["cafe", "capsulas", "compostavel", "eco"],
        "description": "Nespresso-compatible capsules in a fully compostable shell. Convenience without the aluminium guilt.",
    },
    {
        "title": "Cha Preto Orange Pekoe - Gorreana Azores Black Tea",
        "category": "Cha dos Acores",
        "price": "6.90",
        "grammage": "100g",
        "featured": True,
        "tags": ["cha", "preto", "acores", "gorreana", "europa"],
        "description": "Black tea grown on Sao Miguel in the Azores, the only tea plantation in Europe. Orange Pekoe grade, smooth and malty.",
    },
    {
        "title": "Cha Verde Hysson - Azores Green Tea",
        "category": "Cha dos Acores",
        "price": "7.40",
        "grammage": "100g",
        "tags": ["cha", "verde", "acores", "antioxidante"],
        "description": "Azorean green tea, Hysson grade. Grassy and clean, grown in Atlantic volcanic soil without pesticides.",
    },
    {
        "title": "Cha Preto Broken Leaf - Everyday Azores Black Tea",
        "category": "Cha dos Acores",
        "price": "5.90",
        "grammage": "100g",
        "tags": ["cha", "preto", "acores"],
        "description": "Broken-leaf black tea for a stronger, faster brew. The daily cup version of the Orange Pekoe.",
    },
    {
        "title": "Infusao de Cidreira & Limao - Lemon Verbena Herbal Tea",
        "category": "Cha dos Acores",
        "price": "5.20",
        "grammage": "50g",
        "tags": ["cha", "infusao", "sem cafeina", "vegan"],
        "description": "Caffeine-free lemon verbena infusion. Citrusy and calming, good after dinner.",
    },
    {
        "title": "Mel de Rosmaninho DOP - Lavender Honey",
        "category": "Mel & Docaria",
        "price": "9.90",
        "grammage": "500g",
        "featured": True,
        "tags": ["mel", "dop", "rosmaninho", "presente", "natural"],
        "description": "Protected-origin lavender (rosmaninho) honey from inland Portugal. Aromatic and slow to crystallise, a jar worth gifting.",
    },
    {
        "title": "Compota de Frutos Vermelhos - Red Berry Jam",
        "category": "Mel & Docaria",
        "price": "5.50",
        "grammage": "280g",
        "tags": ["compota", "frutos vermelhos", "pequeno-almoco"],
        "description": "Small-batch red berry jam with a high fruit ratio and less sugar than supermarket brands.",
    },
    {
        "title": "Doce de Abobora com Noz - Pumpkin & Walnut Jam",
        "category": "Mel & Docaria",
        "price": "5.20",
        "grammage": "280g",
        "tags": ["doce", "abobora", "noz", "tradicional"],
        "description": "Traditional pumpkin jam studded with walnuts. A Portuguese pantry classic, excellent with cheese.",
    },
    {
        "title": "Marmelada Tradicional - Quince Paste",
        "category": "Mel & Docaria",
        "price": "5.90",
        "grammage": "250g",
        "tags": ["marmelada", "marmelo", "queijo", "tradicional"],
        "description": "Firm quince paste, the original marmalade. Slice it onto a board with cured cheese and walnuts.",
    },
    {
        "title": "Flor de Sal do Algarve - Hand-Harvested Sea Salt Flower",
        "category": "Sal & Especiarias",
        "price": "5.90",
        "grammage": "150g",
        "featured": True,
        "tags": ["sal", "flor de sal", "algarve", "gourmet", "vegan"],
        "description": "Delicate salt crystals hand-skimmed from Algarve salt pans. A finishing salt, not a cooking one.",
    },
    {
        "title": "Flor de Sal com Ervas - Sea Salt Flower with Herbs",
        "category": "Sal & Especiarias",
        "price": "6.50",
        "grammage": "150g",
        "tags": ["sal", "flor de sal", "ervas", "gourmet"],
        "description": "Flor de sal blended with Mediterranean herbs. Finishes grilled fish, meat and vegetables in one step.",
    },
    {
        "title": "Piri-Piri em Flocos - Chilli Flakes",
        "category": "Sal & Especiarias",
        "price": "4.20",
        "grammage": "45g",
        "tags": ["especiaria", "piri-piri", "picante", "vegan"],
        "description": "Dried piri-piri flakes, the backbone of Portuguese heat. For frango, marinades and anything that needs a kick.",
    },
    {
        "title": "Pimenta Preta em Grao - Black Peppercorns",
        "category": "Sal & Especiarias",
        "price": "4.90",
        "grammage": "80g",
        "tags": ["especiaria", "pimenta", "vegan"],
        "description": "Whole black peppercorns for the mill. Fresher and more fragrant than pre-ground.",
    },
    {
        "title": "Cabaz Conservas Gourmet - Tinned Fish Gift Box",
        "category": "Cabazes",
        "price": "32.00",
        "grammage": "4 latas",
        "featured": True,
        "tags": ["cabaz", "presente", "conserva", "gourmet"],
        "description": "A curated box of four premium tins: sardines, tuna, mackerel and octopus. The easiest gift for anyone who loves the sea.",
    },
    {
        "title": "Cabaz Sabores de Portugal - Taste of Portugal Hamper",
        "category": "Cabazes",
        "price": "48.00",
        "grammage": "5 produtos",
        "featured": True,
        "tags": ["cabaz", "presente", "azeite", "mel", "cha", "conserva"],
        "description": "A hamper that tells the whole story: DOP olive oil, lavender honey, Azores tea, flor de sal and a gourmet tin. Made to ship as a gift.",
    },
    {
        "title": "Cabaz Cafe & Cha - Coffee & Tea Discovery Box",
        "category": "Cabazes",
        "price": "26.00",
        "grammage": "4 produtos",
        "featured": True,
        "tags": ["cabaz", "presente", "cafe", "cha"],
        "description": "Specialty coffee, an espresso blend and two Azores teas in one discovery box. For the household split between the kettle and the machine.",
    },
]


class Command(BaseCommand):
    help = "Seed the catalog with Portuguese gourmet products for demand testing"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing products, categories and tags first")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Tag.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Cleared products, categories and tags")

        categories = {}
        for name, ordering in CATEGORIES:
            obj, _ = Category.objects.get_or_create(name=name, defaults={"ordering": ordering})
            if obj.ordering != ordering:
                obj.ordering = ordering
                obj.save()
            categories[name] = obj

        created, updated = 0, 0
        for spec in CATALOG:
            category = categories[spec["category"]]
            existing = Product.objects.filter(title=spec["title"]).first()
            fields = {
                "description": spec["description"],
                "price": Decimal(spec["price"]),
                "grammage": spec["grammage"],
                "category": category,
                "featured": spec.get("featured", False),
                "active": True,
                "quantity": spec.get("quantity", 25),
            }
            if existing:
                for key, value in fields.items():
                    setattr(existing, key, value)
                existing.save()
                product = existing
                updated += 1
            else:
                product = Product.objects.create(title=spec["title"], **fields)
                created += 1

            for tag_title in spec.get("tags", []):
                tag, _ = Tag.objects.get_or_create(title=tag_title)
                tag.products.add(product)

        self.stdout.write(self.style.SUCCESS(
            "Catalog ready: {created} created, {updated} updated, {cats} categories, {tags} tags".format(
                created=created, updated=updated, cats=Category.objects.count(), tags=Tag.objects.count()
            )
        ))
