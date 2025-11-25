import random

class Deck:
    def __init__(self,type: str= "", cards:list[str]=[]):
        if len(cards) == 0:
            if type == "standard":
                suits =["hearts","diamonds","clubs","spades"]
                values = ["2","3","4","5","6","7","8","9","10","jack","queen","king","ace"]
                cards = []
                for s in suits:
                    for v in values:
                        cards.append(v + " of " + s)
                cards.append("joker")
                cards.append('joker')
                self
            else:
                raise ValueError
            self.cards = cards
        else:
            self.cards = cards

    def __str__(self):
        deck_str = ""
        for card in self.cards:
            deck_str += (card + " ")
        return deck_str
    
    def shuffle_deck(self):
        random.shuffle(self.cards)
        return self.cards
    
    def draw(self, number_of_cards : int):
        drawn = []
        for draw in range(number_of_cards):
            ## assumes draw from the top of the deck for now
            card = self.cards[0]
            drawn.append(card)
            self.remove_from_the_deck(card)
        return drawn

    def add_to_deck(self, card_name: str, placement: str = "random"):
        if placement == "top":
            temp_deck =[card_name]
            temp_deck.extend(self.cards)
            self.cards = temp_deck
        elif placement == "bottom":
            temp_deck = self.cards.append(card_name)
            self.cards = temp_deck
        elif placement == "random":
            placement_location = random.randrange(0,len(self.cards))
            temp_deck = self.cards[:placement_location]
            temp_deck.append(card_name)
            temp_deck.extend(self.cards[placement_location:])
            self.cards = temp_deck
        else:
            raise Exception(f"An unknown card placement was requested so no action was taken. {card_name} was not placed at {placement}.")

    def remove_from_the_deck(self, card_name: str):
        try:
            self.cards.remove(card_name)
        except:
            raise Exception(f"{card_name} was requested to be removed from the deck but was not found in the deck so nothing was removed")

    def shuffle_in_discard(self, discard_pile):
        pass

if __name__ == "__main__":
    my_deck = Deck(cards=["two of apples","two of bananas", "two of cherries","two of dates"])
    print(my_deck)
    my_deck.shuffle_deck()
    print(my_deck)
    # print(my_deck.cards)
    # print(my_deck.draw(number_of_cards=1))
    # print(my_deck)
    my_deck.add_to_deck('two of eggplants', placement="banana")
    print(my_deck)