import io
import json
from decimal import Decimal
from pathlib import Path

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from products.models import BundleItem, Category, Product
from tags.models import Tag


SEED_IMAGES = Path(__file__).resolve().parents[2] / "seed_images"
LICENSE_NAMES = {"cc0": "CC0", "pdm": "Public Domain Mark", "by": "CC BY"}
COLLAGE_CREDIT = "Illustrative collage of the items inside"


CATEGORIES = [
    ("Cabazes", "cabazes", "gift", 10),
    ("Cabazes de Natal", "natal", "star", 15),
    ("Conservas", "conservas", "tin", 20),
    ("Azeite & Vinagre", "azeite", "bottle", 30),
    ("Café", "cafe", "coffee", 40),
    ("Chá dos Açores", "cha", "leaf", 50),
    ("Mel & Doçaria", "mel", "jar", 60),
    ("Frutos Secos & Petiscos", "petiscos", "nut", 70),
    ("Sal & Especiarias", "sal", "salt", 80),
    ("Casa & Cortiça", "casa", "cork", 90),
]


def item(title, category, price, grammage, tags, description, featured=False, quantity=25):
    return {
        "title": title,
        "category": category,
        "price": price,
        "grammage": grammage,
        "tags": tags,
        "description": description,
        "featured": featured,
        "quantity": quantity,
    }


CATALOG = [
    item("Cabaz Sabores de Portugal - Taste of Portugal Hamper", "Cabazes", "48.00", "7 produtos",
         ["cabaz", "presente", "gift", "hamper", "azeite", "mel", "chá"],
         "The whole country in one box: DOP olive oil, lavender honey, Azores tea, flor de sal, Azores tuna, quince paste and roasted almonds. Packed to travel as a gift.",
         featured=True, quantity=15),
    item("Cabaz Conservas Gourmet - Tinned Fish Gift Box", "Cabazes", "32.00", "5 latas",
         ["cabaz", "presente", "gift", "conservas", "fish", "sardinha"],
         "Five tins in a gift box: sardines, Azores tuna, octopus, mussels in escabeche and sardine paté. The easy present for anyone who loves the sea.",
         featured=True, quantity=15),
    item("Cabaz Café & Chá - Coffee and Tea Discovery Box", "Cabazes", "26.00", "4 produtos",
         ["cabaz", "presente", "gift", "café", "coffee", "chá", "tea"],
         "Specialty coffee, an espresso blend and two Azores teas. For the household split between the kettle and the machine.",
         featured=True, quantity=15),
    item("Cabaz Petisco Português - Portuguese Snack Box", "Cabazes", "29.00", "6 produtos",
         ["cabaz", "presente", "gift", "petisco", "snack", "azeitonas", "conservas"],
         "Everything for an evening petisco: tinned sardines, Galega olives, roasted Algarve almonds, olive paté, chilli flakes and lupini beans.",
         quantity=15),
    item("Cabaz Pequeno-Almoço - Breakfast Hamper", "Cabazes", "34.00", "6 produtos",
         ["cabaz", "presente", "gift", "breakfast", "mel", "compota", "café"],
         "A slow Portuguese breakfast: heather honey, red berry and fig jams, ground bica coffee, Azores black tea and butter biscuits.",
         quantity=15),
    item("Duo Azeite & Flor de Sal - Olive Oil and Sea Salt Duo", "Cabazes", "19.90", "2 produtos",
         ["cabaz", "presente", "gift", "azeite", "flor de sal"],
         "An early-harvest olive oil paired with hand-harvested Algarve flor de sal. A small gift that gets used every day.",
         quantity=20),

    item("Cabaz de Natal Clássico - Classic Christmas Hamper", "Cabazes de Natal", "59.00", "8 produtos",
         ["natal", "christmas", "cabaz", "presente", "gift"],
         "Olive oil, lavender honey, quince paste, Azores tea, Azores tuna, dark chocolate with flor de sal, roasted almonds and dried figs, in a festive box.",
         featured=True, quantity=20),
    item("Cabaz de Natal Premium - Premium Christmas Hamper", "Cabazes de Natal", "89.00", "7 produtos",
         ["natal", "christmas", "cabaz", "presente", "gift", "premium"],
         "The generous version: early-harvest olive oil, tuna belly, eels in escabeche, São Jorge coffee, two honeys and a cork board.",
         featured=True, quantity=15),
    item("Cabaz de Natal Empresas - Corporate Christmas Hamper", "Cabazes de Natal", "45.00", "por unidade, mín. 10",
         ["natal", "christmas", "empresas", "corporate", "cabaz", "b2b"],
         "For teams and clients, from 10 boxes. Six Portuguese pantry favourites per box, a card with your message and delivery to one or many addresses.",
         featured=True, quantity=100),
    item("Lata Ilustrada de Natal - Illustrated Christmas Tin", "Cabazes de Natal", "16.50", "3 latas",
         ["natal", "christmas", "conservas", "presente", "gift"],
         "Sardines in olive oil, sardines with lemon and mackerel in a limited Christmas illustrated sleeve. A stocking filler that is actually eaten.",
         quantity=30),
    item("Caixa de Chá de Natal - Christmas Tea Box", "Cabazes de Natal", "16.00", "2 x 100g + 50g",
         ["natal", "christmas", "chá", "tea", "açores", "presente"],
         "Black and green tea from the Azores and a lemon verbena infusion in a gift tin for the winter evenings.",
         quantity=30),

    item("Sardinhas em Azeite Extra Virgem - Sardines in Extra Virgin Olive Oil", "Conservas", "6.50", "120g",
         ["conserva", "sardinha", "azeite", "sem glúten"],
         "Whole sardines hand-packed in extra virgin olive oil, in the canning tradition of Matosinhos. Meaty and ready for toasted bread.",
         featured=True),
    item("Cavala em Azeite - Mackerel Fillets in Olive Oil", "Conservas", "5.20", "120g",
         ["conserva", "cavala", "azeite", "sem glúten"],
         "Tender mackerel fillets in olive oil. A lighter, affordable everyday tin with the same Atlantic character.",
         ),
    item("Atum dos Açores em Azeite - Azores Tuna in Olive Oil", "Conservas", "7.90", "120g",
         ["conserva", "atum", "açores", "pesca sustentável"],
         "Pole-and-line skipjack tuna from the Azores in olive oil. Firm, clean and a step above supermarket tuna.",
         featured=True),
    item("Ventresca de Atum - Tuna Belly in Olive Oil", "Conservas", "12.90", "110g",
         ["conserva", "atum", "ventresca", "premium"],
         "The prized belly cut of the tuna, silky and rich. Serve it cold with roasted peppers and good bread.",
         ),
    item("Filetes de Sardinha Picante - Spicy Sardine Fillets", "Conservas", "5.80", "120g",
         ["conserva", "sardinha", "picante", "piri-piri"],
         "Boneless sardine fillets with piri-piri, for anyone who likes some heat with their aperitivo.",
         ),
    item("Sardinhas com Limão - Sardines with Lemon", "Conservas", "6.20", "120g",
         ["conserva", "sardinha", "limão"],
         "Sardines in olive oil with a slice of lemon, bright and fresh-tasting straight from the tin.",
         ),
    item("Polvo em Azeite - Octopus in Olive Oil", "Conservas", "9.50", "120g",
         ["conserva", "polvo", "azeite"],
         "Cooked octopus in olive oil. Serve cold with lemon and coriander or warm over potatoes.",
         ),
    item("Lulas Recheadas - Stuffed Squid in Tomato Sauce", "Conservas", "8.40", "120g",
         ["conserva", "lulas", "tomate"],
         "Small squid stuffed and cooked in a tomato sauce, a full petisco in one tin.",
         ),
    item("Mexilhão em Escabeche - Mussels in Escabeche", "Conservas", "7.50", "110g",
         ["conserva", "mexilhão", "escabeche"],
         "Mussels in a light vinegar and olive oil escabeche with bay leaf. Great with a cold white wine.",
         ),
    item("Enguias de Escabeche - Eels in Escabeche from Aveiro", "Conservas", "11.50", "120g",
         ["conserva", "enguias", "aveiro", "escabeche"],
         "A specialty of the Aveiro lagoon: small eels fried and preserved in escabeche. An unusual, very local tin.",
         ),
    item("Filetes de Bacalhau em Azeite - Cod Fillets in Olive Oil", "Conservas", "9.90", "120g",
         ["conserva", "bacalhau", "cod", "azeite"],
         "Salt cod fillets in olive oil with garlic, ready for a quick salad with chickpeas.",
         ),
    item("Berbigão ao Natural - Cockles in Brine", "Conservas", "6.90", "110g",
         ["conserva", "berbigão", "marisco"],
         "Cockles from the Ria de Aveiro in brine, the base of a quick seafood rice.",
         ),
    item("Ovas de Sardinha - Sardine Roe in Olive Oil", "Conservas", "8.90", "110g",
         ["conserva", "ovas", "sardinha"],
         "A delicacy for the curious: sardine roe in olive oil, creamy and intense.",
         ),
    item("Paté de Sardinha - Sardine Paté", "Conservas", "3.90", "75g",
         ["conserva", "sardinha", "paté", "petisco"],
         "Smooth sardine paté for bread or crackers, the easiest way to bring tinned fish to guests.",
         ),

    item("Azeite Virgem Extra DOP Trás-os-Montes - DOP Extra Virgin Olive Oil", "Azeite & Vinagre", "12.90", "500ml",
         ["azeite", "dop", "trás-os-montes", "olive oil"],
         "Protected-origin extra virgin olive oil from Trás-os-Montes, cold pressed, with a peppery finish for dressing rather than frying.",
         featured=True),
    item("Azeite Virgem Extra do Alentejo - Alentejo Extra Virgin Olive Oil", "Azeite & Vinagre", "14.50", "750ml",
         ["azeite", "alentejo", "olive oil"],
         "Balanced and fruity Alentejo olive oil, the everyday bottle of a Portuguese kitchen.",
         ),
    item("Azeite Colheita Precoce - Early Harvest Olive Oil", "Azeite & Vinagre", "16.90", "500ml",
         ["azeite", "colheita precoce", "premium", "olive oil"],
         "Pressed from green olives at the start of the harvest: grassy, bitter-sweet and high in polyphenols.",
         ),
    item("Azeite Biológico - Organic Extra Virgin Olive Oil", "Azeite & Vinagre", "13.90", "500ml",
         ["azeite", "biológico", "organic", "vegan"],
         "Certified organic extra virgin olive oil from Portuguese groves.",
         ),
    item("Azeite com Piri-Piri - Piri-Piri Olive Oil", "Azeite & Vinagre", "9.50", "250ml",
         ["azeite", "piri-piri", "picante"],
         "Olive oil infused with piri-piri chilli, for grilled chicken, pizza and anything that needs a kick.",
         ),
    item("Azeite com Alho e Ervas - Garlic and Herb Olive Oil", "Azeite & Vinagre", "9.50", "250ml",
         ["azeite", "alho", "ervas"],
         "Olive oil with garlic, rosemary and oregano. Drizzle over bread, potatoes or grilled fish.",
         ),
    item("Vinagre de Vinho do Porto - Port Wine Vinegar", "Azeite & Vinagre", "8.50", "250ml",
         ["vinagre", "porto", "presente"],
         "Vinegar aged from Port wine, deep and slightly sweet. A few drops lift salads and roasted vegetables.",
         ),
    item("Vinagre de Moscatel - Moscatel Vinegar", "Azeite & Vinagre", "9.90", "250ml",
         ["vinagre", "moscatel", "setúbal"],
         "A fragrant, gently sweet vinegar made from Moscatel wine, lovely on fruit and goat cheese.",
         ),

    item("Café Torrado em Grão - Whole Bean Roast", "Café", "7.50", "250g",
         ["café", "grão", "coffee", "espresso"],
         "Classic Portuguese dark roast in whole beans: chocolatey, low in acidity and made for espresso.",
         ),
    item("Café Moído Lote Bica - Ground Espresso Blend", "Café", "6.90", "250g",
         ["café", "moído", "bica", "coffee"],
         "Ready-ground blend for the classic bica, arabica and robusta balanced for crema and body.",
         ),
    item("Café de Especialidade Microlote - Specialty Single Origin", "Café", "11.90", "250g",
         ["café", "especialidade", "coffee", "filter"],
         "A single-origin micro-lot roasted in Lisbon for filter and pour-over. Bright and floral.",
         ),
    item("Café de São Jorge Açores - Azores Island Coffee", "Café", "19.90", "100g",
         ["café", "açores", "são jorge", "raro", "coffee"],
         "Coffee grown on São Jorge island in the Azores, one of the few coffees grown in Europe. Tiny harvest, sweet and mild.",
         ),
    item("Café Lote Lisboa para Moka - Lisbon Moka Pot Blend", "Café", "7.90", "250g",
         ["café", "moka", "coffee"],
         "A medium grind for the stovetop moka pot, roasted a touch lighter for sweetness.",
         ),
    item("Café Descafeinado Moído - Ground Decaf", "Café", "7.20", "250g",
         ["café", "descafeinado", "decaf", "coffee"],
         "Water-process decaf with the body of a real bica, for the evening coffee.",
         ),
    item("Cápsulas Compostáveis - Compostable Coffee Capsules x10", "Café", "4.50", "10 un",
         ["café", "cápsulas", "compostável", "coffee"],
         "Nespresso-compatible capsules in a compostable shell.",
         ),

    item("Chá Preto Orange Pekoe dos Açores - Azores Black Tea", "Chá dos Açores", "6.90", "100g",
         ["chá", "preto", "açores", "tea"],
         "Black tea from São Miguel, one of the few tea plantations in Europe. Orange Pekoe grade, smooth and malty.",
         featured=True),
    item("Chá Verde Hysson dos Açores - Azores Green Tea", "Chá dos Açores", "7.40", "100g",
         ["chá", "verde", "açores", "tea"],
         "Azorean green tea grown in volcanic soil without pesticides. Grassy and clean.",
         ),
    item("Chá Preto Broken Leaf - Everyday Azores Black Tea", "Chá dos Açores", "5.90", "100g",
         ["chá", "preto", "açores", "tea"],
         "Broken-leaf black tea for a stronger, faster brew. The daily cup.",
         ),
    item("Chá Preto de Porto Formoso - Porto Formoso Black Tea", "Chá dos Açores", "7.20", "100g",
         ["chá", "preto", "açores", "porto formoso", "tea"],
         "From the other Azores tea estate, Porto Formoso. Rounder and lightly fruity.",
         ),
    item("Infusão de Lúcia-Lima - Lemon Verbena Infusion", "Chá dos Açores", "5.40", "50g",
         ["infusão", "lúcia-lima", "sem cafeína", "herbal"],
         "Caffeine-free lemon verbena, citrusy and calming after dinner.",
         ),
    item("Infusão de Cidreira & Limão - Lemon Balm and Lemon Infusion", "Chá dos Açores", "5.20", "50g",
         ["infusão", "cidreira", "sem cafeína", "herbal"],
         "Lemon balm with dried lemon peel, a gentle infusion for any time of day.",
         ),
    item("Infusão de Camomila - Chamomile Infusion", "Chá dos Açores", "4.90", "40g",
         ["infusão", "camomila", "sem cafeína", "herbal"],
         "Whole chamomile flowers for a soft, honeyed cup before bed.",
         ),
    item("Lata Presente Chá dos Açores - Azores Tea Gift Tin", "Chá dos Açores", "14.90", "2 x 100g",
         ["chá", "açores", "presente", "gift", "tea"],
         "Orange Pekoe and green tea from the Azores in a keepsake tin.",
         ),

    item("Mel de Rosmaninho DOP - Lavender Honey", "Mel & Doçaria", "9.90", "500g",
         ["mel", "dop", "rosmaninho", "honey"],
         "Protected-origin lavender honey from inland Portugal. Aromatic and slow to crystallise.",
         featured=True),
    item("Mel de Urze - Heather Honey", "Mel & Doçaria", "10.50", "500g",
         ["mel", "urze", "honey"],
         "Dark, malty heather honey from the northern mountains, rich in minerals.",
         ),
    item("Mel de Castanheiro - Chestnut Honey", "Mel & Doçaria", "10.90", "500g",
         ["mel", "castanheiro", "honey"],
         "Bold, slightly bitter chestnut honey, excellent with strong cheese.",
         ),
    item("Mel dos Açores - Azores Honey", "Mel & Doçaria", "11.90", "400g",
         ["mel", "açores", "honey"],
         "Light, floral honey from the Azores islands, gathered from incense tree blossom.",
         ),
    item("Compota de Frutos Vermelhos - Red Berry Jam", "Mel & Doçaria", "5.50", "280g",
         ["compota", "frutos vermelhos", "jam", "breakfast"],
         "Small-batch red berry jam with a high fruit ratio.",
         ),
    item("Compota de Figo - Fig Jam", "Mel & Doçaria", "5.80", "280g",
         ["compota", "figo", "jam", "algarve"],
         "Algarve figs cooked slowly into a thick jam. Perfect on a cheese board.",
         ),
    item("Doce de Abóbora com Noz - Pumpkin and Walnut Jam", "Mel & Doçaria", "5.20", "280g",
         ["doce", "abóbora", "noz", "tradicional"],
         "Traditional pumpkin jam with walnuts, a Portuguese pantry classic.",
         ),
    item("Doce de Tomate - Tomato Jam", "Mel & Doçaria", "5.20", "280g",
         ["doce", "tomate", "tradicional"],
         "Sweet tomato jam with cinnamon, surprising and very Portuguese. Try it with fresh cheese.",
         ),
    item("Marmelada Tradicional - Quince Paste", "Mel & Doçaria", "5.90", "250g",
         ["marmelada", "marmelo", "queijo", "tradicional"],
         "Firm quince paste, the original marmalade. Slice it onto a board with cured cheese.",
         ),
    item("Chocolate Negro com Flor de Sal - Dark Chocolate with Sea Salt", "Mel & Doçaria", "4.90", "100g",
         ["chocolate", "flor de sal", "doce"],
         "70 percent dark chocolate finished with Algarve flor de sal.",
         ),
    item("Bolachas de Manteiga Tradicionais - Traditional Butter Biscuits", "Mel & Doçaria", "4.50", "200g",
         ["bolachas", "biscuits", "doce", "tradicional"],
         "Crisp butter biscuits baked to an old family recipe, made for tea.",
         ),

    item("Amêndoa Torrada do Algarve - Roasted Algarve Almonds", "Frutos Secos & Petiscos", "7.90", "200g",
         ["amêndoa", "algarve", "frutos secos", "snack"],
         "Algarve almonds roasted with a pinch of salt. The classic companion to a glass of wine.",
         ),
    item("Figos Secos do Algarve - Dried Algarve Figs", "Frutos Secos & Petiscos", "6.50", "250g",
         ["figo", "algarve", "frutos secos"],
         "Sun-dried figs from the Algarve, soft and honey-sweet.",
         ),
    item("Amêndoas Cobertas - Sugar-Coated Almonds", "Frutos Secos & Petiscos", "5.90", "200g",
         ["amêndoa", "doce", "tradicional", "páscoa"],
         "Traditional sugar-coated almonds, the sweet of Portuguese Easter and weddings.",
         ),
    item("Azeitonas Galega em Salmoura - Galega Olives in Brine", "Frutos Secos & Petiscos", "4.90", "350g",
         ["azeitonas", "galega", "petisco", "olives"],
         "Small, intense Galega olives, the most Portuguese of olives, cured in brine with oregano.",
         ),
    item("Paté de Azeitona - Olive Paté", "Frutos Secos & Petiscos", "4.20", "100g",
         ["azeitonas", "paté", "petisco", "vegan"],
         "Black olive paté for bread and crackers.",
         ),
    item("Tremoços em Frasco - Lupini Beans in a Jar", "Frutos Secos & Petiscos", "3.50", "350g",
         ["tremoços", "petisco", "snack", "vegan"],
         "The beer snack of every Portuguese café, ready to eat.",
         ),
    item("Mistura de Frutos Secos - Mixed Nuts and Dried Fruit", "Frutos Secos & Petiscos", "6.90", "250g",
         ["frutos secos", "snack", "amêndoa", "figo"],
         "Almonds, walnuts, dried figs and raisins from Portuguese growers.",
         ),

    item("Flor de Sal do Algarve - Hand-Harvested Sea Salt Flower", "Sal & Especiarias", "5.90", "150g",
         ["sal", "flor de sal", "algarve", "vegan"],
         "Delicate salt crystals hand-skimmed from Algarve salt pans. A finishing salt.",
         featured=True),
    item("Flor de Sal com Ervas - Sea Salt Flower with Herbs", "Sal & Especiarias", "6.50", "150g",
         ["sal", "flor de sal", "ervas"],
         "Flor de sal with Mediterranean herbs for grilled fish, meat and vegetables.",
         ),
    item("Flor de Sal com Piri-Piri - Sea Salt Flower with Piri-Piri", "Sal & Especiarias", "6.50", "150g",
         ["sal", "flor de sal", "piri-piri", "picante"],
         "Flor de sal with a warm piri-piri kick.",
         ),
    item("Flor de Sal com Limão - Sea Salt Flower with Lemon", "Sal & Especiarias", "6.50", "150g",
         ["sal", "flor de sal", "limão"],
         "Flor de sal with dried lemon zest, made for fish and salads.",
         ),
    item("Piri-Piri em Flocos - Chilli Flakes", "Sal & Especiarias", "4.20", "45g",
         ["especiaria", "piri-piri", "picante", "vegan"],
         "Dried piri-piri flakes, the backbone of Portuguese heat.",
         ),
    item("Massa de Pimentão - Red Pepper Paste", "Sal & Especiarias", "4.90", "200g",
         ["massa de pimentão", "tempero", "tradicional"],
         "Sweet red pepper paste, the secret of Alentejo pork and roasts.",
         ),
    item("Colorau Doce - Sweet Paprika", "Sal & Especiarias", "3.90", "80g",
         ["colorau", "especiaria", "paprika"],
         "Sweet Portuguese paprika for stews, rice and chouriço dishes.",
         ),
    item("Tempero para Frango Piri-Piri - Piri-Piri Chicken Seasoning", "Sal & Especiarias", "4.50", "60g",
         ["tempero", "piri-piri", "frango"],
         "A ready blend of chilli, garlic, paprika and herbs for piri-piri chicken at home.",
         ),
    item("Pimenta Preta em Grão - Black Peppercorns", "Sal & Especiarias", "4.90", "80g",
         ["especiaria", "pimenta", "vegan"],
         "Whole black peppercorns for the mill.",
         ),

    item("Base de Tacho em Cortiça - Cork Trivet", "Casa & Cortiça", "12.90", "Ø 20 cm",
         ["cortiça", "cork", "casa", "presente"],
         "A thick natural cork trivet. Portugal produces about half of the world's cork.",
         ),
    item("Bases de Copo em Cortiça - Cork Coasters Set of 4", "Casa & Cortiça", "9.90", "4 un",
         ["cortiça", "cork", "casa", "presente"],
         "Four natural cork coasters with a tile-inspired print.",
         ),
    item("Tábua de Queijo em Cortiça - Cork and Wood Cheese Board", "Casa & Cortiça", "24.90", "30 x 20 cm",
         ["cortiça", "cork", "tábua", "presente", "gift"],
         "A wooden cheese board with a cork base, sized for a petisco for four.",
         ),
    item("Sabonete Artesanal de Lavanda - Handmade Lavender Soap", "Casa & Cortiça", "8.90", "150g",
         ["sabonete", "lavanda", "presente", "gift"],
         "Handmade soap with Portuguese lavender, wrapped in printed paper.",
         ),
    item("Azulejo Decorativo Pintado à Mão - Hand-Painted Tile", "Casa & Cortiça", "19.90", "15 x 15 cm",
         ["azulejo", "tile", "decoração", "presente", "gift"],
         "A hand-painted blue and white azulejo with a cork stand.",
         ),
    item("Avental de Linho - Linen Apron", "Casa & Cortiça", "22.90", "1 un",
         ["linho", "avental", "casa", "presente"],
         "A natural linen apron woven in the north of Portugal.",
         ),
    item("Íman Lata de Sardinha - Sardine Tin Magnet", "Casa & Cortiça", "4.90", "1 un",
         ["sardinha", "íman", "presente", "souvenir"],
         "A small illustrated sardine tin magnet for the fridge.",
         ),
]


BUNDLES = {
    "Cabaz Sabores de Portugal": [
        ("Azeite Virgem Extra DOP Trás-os-Montes", 1), ("Mel de Rosmaninho DOP", 1),
        ("Chá Preto Orange Pekoe dos Açores", 1), ("Flor de Sal do Algarve", 1),
        ("Atum dos Açores em Azeite", 1), ("Marmelada Tradicional", 1), ("Amêndoa Torrada do Algarve", 1),
    ],
    "Cabaz Conservas Gourmet": [
        ("Sardinhas em Azeite Extra Virgem", 1), ("Atum dos Açores em Azeite", 1), ("Polvo em Azeite", 1),
        ("Mexilhão em Escabeche", 1), ("Paté de Sardinha", 1),
    ],
    "Cabaz Café & Chá": [
        ("Café de Especialidade Microlote", 1), ("Café Moído Lote Bica", 1),
        ("Chá Preto Orange Pekoe dos Açores", 1), ("Chá Verde Hysson dos Açores", 1),
    ],
    "Cabaz Petisco Português": [
        ("Sardinhas em Azeite Extra Virgem", 1), ("Azeitonas Galega em Salmoura", 1),
        ("Amêndoa Torrada do Algarve", 1), ("Paté de Azeitona", 1), ("Piri-Piri em Flocos", 1),
        ("Tremoços em Frasco", 1),
    ],
    "Cabaz Pequeno-Almoço": [
        ("Mel de Urze", 1), ("Compota de Frutos Vermelhos", 1), ("Compota de Figo", 1),
        ("Café Moído Lote Bica", 1), ("Chá Preto Orange Pekoe dos Açores", 1),
        ("Bolachas de Manteiga Tradicionais", 1),
    ],
    "Duo Azeite & Flor de Sal": [
        ("Azeite Colheita Precoce", 1), ("Flor de Sal do Algarve", 1),
    ],
    "Cabaz de Natal Clássico": [
        ("Azeite Virgem Extra do Alentejo", 1), ("Mel de Rosmaninho DOP", 1), ("Marmelada Tradicional", 1),
        ("Chá Preto Orange Pekoe dos Açores", 1), ("Atum dos Açores em Azeite", 1),
        ("Chocolate Negro com Flor de Sal", 1), ("Amêndoa Torrada do Algarve", 1), ("Figos Secos do Algarve", 1),
    ],
    "Cabaz de Natal Premium": [
        ("Azeite Colheita Precoce", 1), ("Ventresca de Atum", 1), ("Enguias de Escabeche", 1),
        ("Café de São Jorge Açores", 1), ("Mel dos Açores", 1), ("Mel de Castanheiro", 1),
        ("Tábua de Queijo em Cortiça", 1),
    ],
    "Cabaz de Natal Empresas": [
        ("Azeite Virgem Extra DOP Trás-os-Montes", 1), ("Mel de Rosmaninho DOP", 1),
        ("Chá Preto Orange Pekoe dos Açores", 1), ("Sardinhas em Azeite Extra Virgem", 1),
        ("Chocolate Negro com Flor de Sal", 1), ("Flor de Sal do Algarve", 1),
    ],
    "Lata Ilustrada de Natal": [
        ("Sardinhas em Azeite Extra Virgem", 1), ("Sardinhas com Limão", 1), ("Cavala em Azeite", 1),
    ],
    "Caixa de Chá de Natal": [
        ("Chá Preto Orange Pekoe dos Açores", 1), ("Chá Verde Hysson dos Açores", 1),
        ("Infusão de Lúcia-Lima", 1),
    ],
}


def credit_text(credit):
    license_name = LICENSE_NAMES.get(credit.get("license"), (credit.get("license") or "").upper())
    if credit.get("license") == "by" and credit.get("license_version"):
        license_name = "{name} {version}".format(name=license_name, version=credit["license_version"])
    source = (credit.get("source") or "").replace("_", " ").title()
    creator = credit.get("creator") or "unknown author"
    return "{creator} / {source}, {license}".format(creator=creator, source=source, license=license_name)[:300]


def fit(img, width, height):
    ratio = width / height
    w, h = img.size
    if w / h > ratio:
        new_w = int(h * ratio)
        img = img.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:
        new_h = int(w / ratio)
        img = img.crop((0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h))
    return img.resize((width, height), Image.LANCZOS)


def collage(paths, size=(800, 600), gap=6, background=(244, 237, 224)):
    count = len(paths)
    width, height = size
    rows = [count] if count <= 3 else [count // 2, count - count // 2]
    canvas = Image.new("RGB", size, background)
    row_height = (height - gap * (len(rows) + 1)) // len(rows)
    index, y = 0, gap
    for per_row in rows:
        tile_width = (width - gap * (per_row + 1)) // per_row
        x = gap
        for _ in range(per_row):
            with Image.open(paths[index]) as source:
                canvas.paste(fit(source.convert("RGB"), tile_width, row_height), (x, y))
            x += tile_width + gap
            index += 1
        y += row_height + gap
    return canvas


class Command(BaseCommand):
    help = "Seed the catalog with Portuguese gourmet products for demand testing"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing products, categories and tags first")
        parser.add_argument("--refresh-images", action="store_true", help="Re-attach photos and rebuild hamper collages")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Tag.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Cleared products, categories and tags")

        categories = {}
        for name, slug, icon, ordering in CATEGORIES:
            obj, _ = Category.objects.get_or_create(name=name, defaults={"ordering": ordering, "slug": slug, "icon": icon})
            changed = False
            for field, value in (("ordering", ordering), ("slug", slug), ("icon", icon)):
                if getattr(obj, field) != value:
                    setattr(obj, field, value)
                    changed = True
            if changed:
                obj.save()
            categories[name] = obj

        created, updated = 0, 0
        for spec in CATALOG:
            fields = {
                "description": spec["description"],
                "price": Decimal(spec["price"]),
                "grammage": spec["grammage"],
                "category": categories[spec["category"]],
                "featured": spec["featured"],
                "active": True,
                "quantity": spec["quantity"],
            }
            product = Product.objects.filter(title=spec["title"]).first()
            if product:
                for key, value in fields.items():
                    setattr(product, key, value)
                product.save()
                updated += 1
            else:
                product = Product.objects.create(title=spec["title"], **fields)
                created += 1

            for tag_title in spec["tags"]:
                tag, _ = Tag.objects.get_or_create(title=tag_title)
                tag.products.add(product)

        catalog_titles = {spec["title"] for spec in CATALOG}
        by_primary = {p.title_primary: p for p in Product.objects.all() if p.title in catalog_titles}
        self.build_bundles(by_primary)
        photos = self.attach_photos(by_primary.values(), options["refresh_images"])
        collages = self.attach_collages(by_primary, options["refresh_images"])

        self.stdout.write(self.style.SUCCESS(
            "Catalog ready: {created} created, {updated} updated, {cats} categories, {tags} tags, "
            "{bundles} hampers, {photos} photos attached, {collages} collages built".format(
                created=created, updated=updated, cats=Category.objects.count(), tags=Tag.objects.count(),
                bundles=len(BUNDLES), photos=photos, collages=collages,
            )
        ))

    def build_bundles(self, by_primary):
        for bundle_title, lines in BUNDLES.items():
            bundle = by_primary[bundle_title]
            BundleItem.objects.filter(bundle=bundle).delete()
            for item_title, quantity in lines:
                BundleItem.objects.create(bundle=bundle, item=by_primary[item_title], quantity=quantity)
            if bundle.bundle_saving <= 0:
                self.stderr.write("{title}: items cost {value} EUR, not more than the hamper price {price} EUR".format(
                    title=bundle_title, value=bundle.bundle_value, price=bundle.price))

    def attach_photos(self, products, refresh):
        credits_path = SEED_IMAGES / "credits.json"
        credits = json.loads(credits_path.read_text(encoding="utf-8")) if credits_path.exists() else {}
        attached = 0
        for product in products:
            key = slugify(product.title)
            path = SEED_IMAGES / (key + ".jpg")
            if not path.exists() or (product.image and not refresh):
                continue
            with path.open("rb") as handle:
                product.image.save(path.name, File(handle), save=False)
            credit = credits.get(key, {})
            product.image_credit = credit_text(credit) if credit else ""
            product.image_source_url = credit.get("landing_url", "")
            product.image_license_url = credit.get("license_url", "")
            product.save()
            attached += 1
        return attached

    def attach_collages(self, by_primary, refresh):
        built = 0
        for bundle_title in BUNDLES:
            bundle = by_primary[bundle_title]
            if bundle.image and not refresh:
                continue
            paths = [line.item.image.path for line in bundle.bundle_items.select_related("item") if line.item.image]
            if not paths:
                continue
            buffer = io.BytesIO()
            collage(paths).save(buffer, "JPEG", quality=82, optimize=True, progressive=True)
            bundle.image.save(slugify(bundle.title) + ".jpg", ContentFile(buffer.getvalue()), save=False)
            bundle.image_credit = COLLAGE_CREDIT
            bundle.image_source_url = ""
            bundle.image_license_url = ""
            bundle.save()
            built += 1
        return built
