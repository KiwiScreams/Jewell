from ext import app, db
from models import Product, User
with app.app_context():
    db.drop_all()
    db.create_all()
    admin_user = User(
        firstname="Admin",
        lastname="Admin",
        email="admin@example.com",
        phone_number="1234567890",
        password="adminpassword",
        gender="Other",
        country="CountryName",
        role="Admin"
    )
    ava_levis = User(
        firstname="Ava",
        lastname="Lewis",
        email="ava@gmail.com",
        phone_number="557585859",
        password="123456789",
        gender="Female",
        country="Mexico",
        role="User"
    )
    haruto_tanaka = User(
        firstname="Haruto",
        lastname="Tanaka",
        email="tanaka@gmail.com",
        phone_number="11125879",
        password="987654321",
        gender="Male",
        country="Japan",
        role="User"
    )
    sakura_yamamoto = User(
        firstname="Sakura",
        lastname="Yamamoto",
        email="sakura@gmail.com",
        phone_number="11125879",
        password="987654321",
        gender="Female",
        country="Japan",
        role="User"
    )
    admin_user.save()
    sakura_yamamoto.save()
    haruto_tanaka.save()
    ava_levis.save()

    diamond_ring = Product(
        name="Diamond Ring",
        price=1500,
        image_url="image 56.png",
        description="A beautiful diamond ring with a gold band, perfect for engagements or special occasions.",
        quantity=25,
        brand="Luxury Jewels",
        material="Gold",
        category="Rings"
    )
    diamond_ring.save()


    sapphire_ring = Product(
        name="Sapphire Ring",
        price=1800,
        image_url="image 61.png",
        description="A stunning sapphire engagement ring with a platinum band, a timeless symbol of love and commitment.",
        quantity=15,
        brand="Elegant Gems",
        material="Platinum",
        category="Rings"
    )
    sapphire_ring.save()


    emerald_ring = Product(
        name="Emerald Promise Ring",
        price=1300,
        image_url="pngwing.com (4).png",
        description="A beautifully crafted emerald promise ring with a sterling silver band, perfect for any occasion.",
        quantity=30,
        brand="Prestige Jewelry",
        material="Zinc",
        category="Rings"
    )
    emerald_ring.save()


    gold_emerald_bracelet = Product(
        name="Gold Emerald Bracelet",
        price=2500,
        image_url="pngwing.com (8).png",
        description="A luxurious gold bracelet with emerald stones, designed for elegance and style.",
        quantity=20,
        brand="Royal Jewels",
        material="Gold",
        category="Gift"
    )
    gold_emerald_bracelet.save()


    gold_emerald_ring = Product(
        name="Gold Emerald Ring",
        price=1800,
        image_url="pngwing.com (6).png",
        description="A stunning gold ring featuring a beautiful emerald stone, perfect for any occasion.",
        quantity=15,
        brand="Royal Jewels",
        material="Gold",
        category="Rings"
    )
    gold_emerald_ring.save()


    gold_emerald_earrings = Product(
        name="Gold Emerald Earrings",
        price=1500,
        image_url="pngwing.com (10).png",
        description="Elegant gold earrings with sparkling emerald stones, designed for a chic and refined look.",
        quantity=30,
        brand="Royal Jewels",
        material="Gold",
        category="Earrings"
    )
    gold_emerald_earrings.save()


    gold_emerald_necklace = Product(
        name="Gold Emerald Necklace",
        price=3200,
        image_url="pngwing.com (5).png",
        description="A luxurious gold necklace with a striking emerald pendant, crafted for sophistication.",
        quantity=10,
        brand="Royal Jewels",
        material="Gold",
        category="Gift"
    )
    gold_emerald_necklace.save()

    platinum_sapphire_ring = Product(
        name="Platinum Sapphire Ring",
        price=3500,
        image_url="pngwing.com (10).png",
        description="An elegant platinum ring featuring a brilliant sapphire stone, designed for luxury.",
        quantity=12,
        brand="Royal Jewels",
        material="Platinum",
        category="Rings"
    )
    platinum_sapphire_ring.save()

    silver_diamond_earrings = Product(
        name="Silver Diamond Earrings",
        price=2200,
        image_url="pngwing.com (3).png",
        description="Sparkling diamond earrings set in sterling silver, perfect for formal events or daily wear.",
        quantity=25,
        brand="Royal Jewels",
        material="Silver",
        category="Earrings"
    )
    silver_diamond_earrings.save()

    rose_gold_ruby_necklace = Product(
        name="Rose Gold Ruby Necklace",
        price=2800,
        image_url="pngwing.com (5).png",
        description="A luxurious rose gold necklace adorned with a stunning ruby pendant, exuding elegance.",
        quantity=8,
        brand="Royal Jewels",
        material="Rose Gold",
        category="Bracelets"
    )
    rose_gold_ruby_necklace.save()

    white_gold_pearl_ring = Product(
        name="White Gold Pearl Ring",
        price=1600,
        image_url="pngwing.com (7).png",
        description="A delicate white gold ring featuring a lustrous pearl, designed for refined tastes.",
        quantity=20,
        brand="Royal Jewels",
        material="White Gold",
        category="Rings"
    )
    white_gold_pearl_ring.save()