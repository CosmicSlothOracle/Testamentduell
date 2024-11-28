from .constants import *

class Player:
    MAX_HAND_SIZE = 5  # Example value

    def __init__(self, name, deck):
        """Initialize a player with a name and a deck of cards."""
        self.name = name
        self.deck = deck
        self.hand = []        self.sanctuary = []
        self.mission_cards = []
        self.grace_points = STARTING_GRACE_POINTS
        self.max_skp = STARTING_SKP
        self.current_skp = STARTING_SKP
        
    def draw_card(self):
        """Draw a card from the deck to the hand, if possible."""
        if len(self.hand) >= self.MAX_HAND_SIZE:
            print(f"{self.name}'s hand is full!")
            return False
            
        if not self.deck:
            print(f"{self.name}'s deck is empty!")
            return False
            
        card = self.deck.pop(0)
        self.hand.append(card)
        return True
        
    def play_card(self, card_index: int, zone: str) -> bool:
        """Play a card from hand to a specific zone"""
        if card_index >= len(self.hand):
            return False
            
        card = self.hand[card_index]
        
        # Check zone-specific conditions
        if zone == 'SANCTUARY':
            if len(self.sanctuary) >= MAX_SANCTUARY_SIZE:
                print(f"{self.name}'s sanctuary is full!")
                return False
                
            if self.current_skp >= card.skp_cost:
                self.current_skp -= card.skp_cost
                self.sanctuary.append(self.hand.pop(card_index))
                print(f"{self.name} played {card.name} to sanctuary")
                return True
            else:
                print(f"Not enough SKP to play {card.name}")
                
        return False
