from pokemontcgsdk import Card
from pokemontcgsdk import Set

# export POKEMONTCG_IO_API_KEY=

# set = Set.find("base1")
# print(set.id)
# print(set.name)

# cards = Card.where(q=f"set.id:{set.id}")
# print(len(cards))

card = Card.find("base1-1")
print(card)
print(card.prices)

