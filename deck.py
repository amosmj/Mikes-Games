import random
import logging

## modules in this script
import card

class Deck:
    def __init__(self,type: str= "", cards:list[str]=[], players_can_see: bool = True):
        self.players_can_see = players_can_see
        if len(cards) == 0:
            ## When a card list is not passed it is assumed that you want some kind of standard list
            if type == "standard":
                suits =["hearts","diamonds","clubs","spades"]
                values = ["2","3","4","5","6","7","8","9","10","jack","queen","king","ace"]
                cards = []
                for s in suits:
                    for v in values:
                        cards.append(card.Card(name= v + " of " + s, suit = s, face= v))
                        # cards.append(v + " of " + s)C
                # cards.append("joker")
                # cards.append('joker')
                cards.append(card.Card(name = "joker"))
                cards.append(card.Card(name = "joker"))
            else:
                logging.debug("No list was passed so I checked for standard deck types. " \
                "No deck type was recognized so I am passing an empty list as the deck. " \
                "The assumption is that this is a placeholder and will be populated in game.")
        else:
            logging.debug("A list was passed so I'm turning that into the deck. " \
            "No type checking for cards has been done.")
            # logging.debug(cards)
        # print("passed both elses")
        self.cards = cards
        logging.debug(self)

    def __str__(self):
        deck_str = ""
        if self.players_can_see:
            for card in self.cards:
                # logging.debug(card.name)
                # logging.debug(type(card))
                deck_str += (card.name + " ")
        else:
            deck_str = "You aren't allowed to look in that deck."
        return deck_str
    
    def shuffle_deck(self):
        random.shuffle(self.cards)
        return self.cards
    
    def draw(self, number_of_cards : int= 1):
        drawn = Deck()
        ## need to build test for drawing more cards than are in the deck
        for draw in range(number_of_cards):
            ## assumes draw from the top of the deck for now
            card = self.cards[0]
            logging.debug(f"You drew: {card}")
            drawn.add_to_deck(card= card)
            self.remove_from_the_deck(card)
        logging.debug(drawn)
        logging.debug(self)
        return drawn

    def add_to_deck(self, card: card.Card, placement: str = "random"):
        try:
            logging.debug(f"Deck contains {len(self.cards)}")
        except:
            logging.debug("You're adding something to an empty deck")
            temp_deck=Deck()

        if len(self.cards) == 0:
            logging.debug(f"You are adding {card} to and empty deck")
            temp_deck = [card]
        elif placement == "top":
            logging.debug(f"You are adding {card} to the top of your deck")
            temp_deck = [card]
            temp_deck.extend(self.cards)
            # self.cards = temp_deck
        elif placement == "bottom":
            logging.debug(f"You are adding {card} to the bottom of your deck")
            temp_deck = self.cards
            temp_deck.append(card)
            # self.cards = temp_deck
        elif placement == "random":
            logging.debug(f"You are adding {card} to a random place in your deck")
            placement_location = random.randrange(0,len(self.cards))
            temp_deck = self.cards[:placement_location]
            temp_deck.append(card)
            temp_deck.extend(self.cards[placement_location:])
            # self.cards = temp_deck
        else:
            raise Exception(f"An unknown card placement was requested so no action was taken. {card} was not placed at {placement}.")
        self.cards = temp_deck

    def remove_from_the_deck(self, card_name: str):
        try:
            self.cards.remove(card_name)
        except:
            raise Exception(f"{card_name} was requested to be removed from the deck but was not found in the deck so nothing was removed")

    def shuffle_in_discard(self, discard_pile):
        pass

    def cut_the_deck(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    my_deck = Deck(cards=[card.Card(name="two of apples"),card.Card(name="two of bananas")
                          , card.Card(name="two of cherries"),card.Card(name="two of dates")], players_can_see=False)
    logging.info(f"Built my little deck: {my_deck}")
    my_deck.players_can_see=True
    logging.info(f"Now I can see my little deck: {my_deck}")
    my_deck.shuffle_deck()
    logging.info(f"Shuffled my little deck: {my_deck}")
    hand = my_deck.draw(number_of_cards=1)
    logging.info(f"My hand consists of {hand}")
    logging.info(f"The deck consists of {my_deck}")
    my_deck.add_to_deck(card.Card(name="two of eggplants"), placement="top")
    logging.info(my_deck)
    my_deck.add_to_deck(card.Card(suit="figs", face="two"), placement="bottom")
    logging.info(my_deck)
    my_deck.add_to_deck(card.Card(suit="grapes", face="two"))
    logging.info(my_deck)

    # new_deck = Deck(type="standard")
    # new_deck.shuffle_deck()
    # print(new_deck)