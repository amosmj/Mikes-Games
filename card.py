class Card:
    def __init__(self, name:str = None, suit: str = None, face: str = None, **kwargs):
        """
        Creates a card.

        :param name: If no name is provided one will be made from 
            combining the suit and face
        :type name: str
        :param suit: Use to describe any grouper of values. For example: 
            Spades and Hearts for a standard deck of playing cards. You 
            could also use something like a color name for a game like 
            Uno. In a game with no suits/colors or where they don't matter
            you can leave this as None.
        :type suit: str
        :param face: Describe the face value of the card as a string. So you 
            can make the 2 in a standard deck of cards either "2" or "two" 
            but not 2.
        :type face: str
        :param kwargs: Pass a dictionary of other card attributes. Common ones 
            may include things like:
            value = integer value thata card scores as
            wild = boolean value to indicate that this care can sub in
                for any other card
        """
        self.suit = suit
        self.face = face
        for key, val in kwargs.items():
            setattr(self, key, val)

        if name is None:
            try:
                self.name = f"{face} of {suit}"
            except:
                raise ValueError("You attempted to create a card with no name " \
                "and it also did not have a value and face. You either need a " \
                "name or both a value and face")
        else:
            self.name = name

    def __del__(self):
        """placeholder in case I want to take any action on card destruction"""
        pass

    def __str__(self):
        return self.name

    def modify(self, **kwargs):
        """
        I'm placing this here to remind myself that I want to do this. 
        Process is TBD. I think I want to take arbitrary kwargs, test to 
        see if the old keyword exists and if so, test that the new value 
        is of the same type then replace. If it's not there then insert 
        it. Conceptually this feels prone to abuse but that probably 
        doesn't matter.
        I want to, hypothetically, be able to assign wil cards during a game
        I also like the idea of a made up game where the attributes of the
        cards can change in the course of the game
        
        :param self: Description
        :param kwargs: Description
        """

    def destroy(self):
        """
        Use destroy() to remove a card. Need to tes this inside a deck or hand
        """
        del self

if __name__ == "__main__":
    my_card = Card(name = "My First Card", suit= "Clubs", face= "Jack")
    print(my_card)
    print(my_card.suit)
    my_card.points = 13
    print(my_card.points)
    my_card.name = "The same card"
    print(my_card)