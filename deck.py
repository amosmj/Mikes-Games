import random
import logging

## modules in this script
import card

class Deck:
    """
    Deck is a container/group/packet of cards

    Arguments:
    type: An optional string that describes how the deck can be used. 
        This is limited to whatever types I have come up with for now:
        draw - think of the draw pile in most games, face-down, not 
            browseable, can be drawn from, usually drawn until exhauseted
        discard - usually face up and public, often browseable, arbitrarily shuffled
            and added to a draw pile
        hand - usually face up but private, usually browseable, usually 
            cards can be drawn arbitrarily
        none - default value, behaves like a draw pile by default
    
    kwargs: In the event that one of the above deck types doesn't do everything
        that you need you can build your own type or overwrite the default
        values on one of those types. Here is a list of the keywords I 
        am thinking you will send:
        owner
        who_can_browse - a list of players who are allowed to know what 
            cards are in the deck and in what order
        who_can_sort - a list of players who are allowed to change the
            order of cards
        who_can_draw - a list of players who are allowed to remove
            cards from them deck, into their hand
    """
    def __init__(self,type: str= "", cards: str|list[str]=[], **kwargs):
        ## note to self, do I need to abstract out creating the deck object from populating the deck object
        if type == 'draw':
            logging.debug("Creating a deck as a draw pile")
            self.owner = []
            self.who_can_browse = []
            self.who_can_sort = []
            ## need to come back to this after I introduce the game and players as objects. 
            self.who_can_draw = []
            self.who_can_play = []
        elif type == 'discard':
            logging.debug("Creating a deck as a discrd pile")
            self.owner = "everyone"
            self.who_can_browse = "everyone"
            self.who_can_sort = []
            self.who_can_draw = []
            self.who_can_play = []
        elif type == 'hand':
            logging.debug("Creating a deck as a hand")
            ## need to come back to this after I introduce the game and players as objects. 
            self.owner = []
            self.who_can_browse = []
            self.who_can_sort = []
            self.who_can_draw = []
            self.who_can_play = []
        elif type == "" or type is None:
            logging.debug("Creating a deck and in else where you should be manually assigning attributes")
        else:
            raise ValueError(f"A {type} deck was requested but that value is" \
                             "not recognized. You will need to pass a know type " \
                             "or pass the attributes in kwargs")
        ## assigning attributes here. I want them to overwrite the default attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        
        ## need to move this into the either the add cards method or create a distinct
        ## populate_deck method
        if isinstance(cards, str):
            ## When a card list is not passed it is assumed that you want some kind of standard list
            if cards == "standard":
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
        elif isinstance(cards, list):
            logging.debug("A list was passed so I'm turning that into the deck. " \
            "No type checking for cards has been done.")
            ## ad type checking, if it's a card, pass add it to the deck as a card, if it's
            ## a string, add it as a card with the string's name
            # logging.debug(cards)
        # print("passed both elses")
        else:
            raise TypeError(f"A {type(cards)} object was passed to create a deck but it doesn't know what to do with it")
        self.cards = cards
        logging.debug(self)

    def __str__(self):
        deck_str = ""
        for card in self.cards:
            # logging.debug(card.name)
            # logging.debug(type(card))
            deck_str += (card.name + " ")
        return deck_str
    
    def __add__(self,other):
        """
        This function is not yet tested. Need to make sure it works as intended
        
        :param self: Description
        :param other: Description
        """
        if isinstance(other, card.Card):
            self.cards.append(other)
        elif isinstance(other, Deck):
            self.cards.extend(other.cards)
        else:
            raise TypeError(f"You tried to add a {type(other)} to a Deck. This is not yet supported")
    
    def shuffle_deck(self):
        """
        Use shuffle on a deck to randomize it.
        """
        random.shuffle(self.cards)
        return self.cards
    
    def draw(self, number_of_cards : int= 1):
        """
        Draws X cards from thr "top" of the deck
        
        :param number_of_cards: (default: 1) Pass an integer to draw that many cards from the deck
        :type number_of_cards: int
        """
        drawn = Deck()
        ## need to build test for drawing more cards than are in the deck
        for draw in range(number_of_cards):
            ## assumes draw from the top of the deck for now
            card = self.cards[0]
            logging.debug(f"You drew: {card}")
            drawn.add_a_card_to_deck(card= card)
            self.remove_from_the_deck(card)
        logging.debug(drawn)
        logging.debug(self)
        return drawn

    def add_to_deck(self, cards: card.Card| Deck | str | None, placement: str = "random"):
        """
        Courtesty function to make it esier to add any number of cards to a deck
        This functon will parse out which supporting method it needs to go to
        then send your call there
        
        :param cards: pass a card, a deck, a string, a list of cards, or a list of strings

        :type cards: card.Card | Deck | str | None
        
        :param placement: Description: pass a valid string and all of the cards will be
            placed in this fasion

            Valid Strings:
            * "random" (default) - each card will be placed randomly. This does not
                currently support placing a paced together randomly
            * "top"  - places all cards on top of the pile. This method
                currently reverses the order because each card is placed
                in turn rather than as a packet.
            * "bottom" - places all cards on the bottom of the pile, card 0 
                should be at position len of the deck its being added to
        """
        ## check self to make sure you exist
        try:
            logging.debug(f"Deck contains {len(self.cards)}")
        except:
            logging.debug("You're adding something to an empty deck")
            temp_deck=Deck()

        ## determine how many cards and in what format and add
        if isinstance(cards, card.Card):
            logging.debug("add_to_deck received a single card.Card. " \
                "Passing to add_a_card_to_Deck")
            self.add_a_card_to_deck(card= cards, placement = placement)
        elif isinstance(cards,Deck):
            logging.debug("add_to_deck received a Deck object. " \
                "Passing to add_multiple_cards_to_deck")
            self.add_multiple_cards_to_deck(cards= cards, placement=placement)
        elif isinstance(cards,list) or isinstance(cards,dict):
            logging.debug("add_to_Deck received a list or dictionary. " \
                "Assessing for number of contained objects")
            if len(cards) > 1:
                logging.debug("add_to_deck assessed the list or dictionary and " \
                    "found it had multiple objects. Passing to add_multipe_cards_to_deck")
                self.add_multiple_cards_to_deck(cards= cards, placement=placement)
            elif len(cards) == 1:
                logging.debug("add_to_deck assessed the list or dictionary and " \
                    "found it had one object. Passing to add_a_card_to_deck")
                self.add_a_card_to_deck(card= cards, placement = placement)
            else:
                raise Exception("It looks like an empty list was passed to be added " \
                "to a deck. Nothing was added")
        else:
            raise Exception("An object type was passedto add_to_deck that it doesn't " \
            "know how to handle so nothing was added.")

    def add_multiple_cards_to_deck(self, cards: card.Card| Deck | str, placement: str = "random"):
        """
        Pass this functon deck of cards or a list of cards and it will unbundle 
        them and handle passing them one at a time to add_a_card_to_deck.
        
        :param cards: designed to take a Deck of cards or a list of cards. 
        :type cards: card.Card | Deck | str
    
        :param placement: Description: pass a valid string and all of the cards will be
            placed in this fasion
            Valid Strings:
            "random" (default) - each card will be placed randomly. This does not
                currently support placing a paced together randomly
            "top"  - places all cards on top of the pile. This method
                currently reverses the order because each card is placed
                in turn rather than as a packet.
            "bottom" - places all cards on the bottom of the pile, card 0 
                should be at position len of the deck its being added to
        """
        if isinstance(cards, Deck):
            for card in cards.cards:
                logging.debug(f"unpack deck, currently: {card}")
                self.add_a_card_to_deck(card = card, placement= placement)
        elif isinstance(cards, list):
            for thing in cards:
                if isinstance(thing, card.Card):
                    self.add_a_card_to_deck(card = card, placement= placement)
                elif isinstance(thing, str):
                    new_card = card.Card(name=thing)
                    self.add_a_card_to_deck(card= new_card, placement=placement)
                elif isinstance(thing, dict):
                    new_card = card.Card(**thing)
                    self.add_a_card_to_deck(card= new_card, placement= placement)
                else:
                    raise TypeError("An object of an unsupported type was " \
                        "attempt to be used to create a card and addit to a deck."
                        " Interrupting this program")
        else:
            raise TypeError("An object of an unsupported type was attempted to " \
            "be added to a deck. Interrupting this program")

    def add_a_card_to_deck(self, card, placement: str = "random"):    
        """
        Place a single card n a deck. 
        
        :param self: Description
        :param card: Description
        :param placement: Description
        :type placement: str
        """

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

def test_with_custom_deck():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    my_deck = Deck(cards=[card.Card(name="two of apples"),card.Card(name="two of bananas")
                        , card.Card(name="two of cherries"),card.Card(name="two of dates")])
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
    new_deck = Deck(cards=[card.Card(name="three of apples"),card.Card(suit="apples", face="four")])
    logging.info(new_deck)
    my_deck.add_to_deck(cards=new_deck)
    logging.info(my_deck)
    new_deck = Deck(cards=[card.Card(name="three of bananas"),card.Card(suit="bananas", face="four")])
    logging.info(new_deck)
    my_deck.add_to_deck(cards=new_deck,placement="top")
    logging.info(my_deck)
    new_deck = Deck(cards=[card.Card(name="three of cherries"),card.Card(suit="cherries", face="four")])
    logging.info(new_deck)
    my_deck.add_to_deck(cards=new_deck,placement="bottom")
    logging.info(my_deck)



def test_with_standard_deck():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    standard_deck = Deck(cards="standard")
    standard_deck.shuffle_deck()
    logging.info(standard_deck)
                                
if __name__ == "__main__":
    test_with_custom_deck()
    # test_with_standard_deck()