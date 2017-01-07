from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create default owner for all items
test_user = User(name="Han Solo", email="han_solo@test.com", id="1")
session.add(test_user)
session.commit()

# Soccer category and items
cat1 = Category(name="Soccer")

session.add(cat1)
session.commit()

item1 = Item(name="Mouthguard", description="Snug, comfortable mold of your teeth ensuring a slip-proof fit.", category=cat1, user=test_user)

session.add(item1)
session.commit()

item2 = Item(name="Shinguards", description="High quality polycarbonate.",category=cat1, user=test_user)

session.add(item2)
session.commit()

item3 = Item(name="Cleats", description="Thick tread ensures utmost traction on turf.",
                     category=cat1, user=test_user)

session.add(item3)
session.commit()


# Basketball category and items
cat2 = Category(name="Basketball")

session.add(cat2)
session.commit()

item1 = Item(name="High tops", description="Stylish, comfortable and functional.", category=cat2, user=test_user)

session.add(item1)
session.commit()

item2 = Item(
    name="Goggles", description="Quality lenses ensures utmost clarity and eye protection.", category=cat2, user=test_user)

session.add(item2)
session.commit()

item3 = Item(name="Arm sleeves", description="Superior protection so you can play fearlessly on the court", category=cat2, user=test_user)

session.add(item3)
session.commit()


# Baseball category and items
cat3 = Category(name="Baseball")

session.add(cat3)
session.commit()


item1 = Item(name="Cup", description="Take no chances with this thick, padded cup.", category=cat3, user=test_user)

session.add(item1)
session.commit()

item2 = Item(name="Leather glove", description="Made from the finest cows.", category=cat3, user=test_user)

session.add(item2)
session.commit()

item3 = Item(name="Cap", description="Wide brimmed with breathable nylon.", category=cat3, user=test_user)

session.add(item3)
session.commit()


# Snowboarding category and items
cat4 = Category(name="Snowboarding")

session.add(cat4)
session.commit()


item1 = Item(name="Bindings", description="Patented locking mechanism.", category=cat4, user=test_user)

session.add(item1)
session.commit()

item2 = Item(name="Snowboard", description="Best for any terrain and conditions.", category=cat4, user=test_user)

session.add(item2)
session.commit()

item3 = Item(name="Boots", description="Light and anti-fungal.", category=cat4, user=test_user)

session.add(item3)
session.commit()

print "added menu items!"