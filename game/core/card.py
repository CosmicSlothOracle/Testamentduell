import pygame
from .constants import (
    CARD_WIDTH, 
    CARD_HEIGHT, 
    BLACK, 
    GOLD, 
    WHITE,
    DARK_BLUE
)
from .types import Position, CardType, Faction
from ..effect_system import Effect, Timing

class Card:
    def __init__(self, name, card_type, effect, attribute=None, image_path=None, 
                 level=None, faith_points=None, divinity_points=None,
                 scripture_type=None, miracle_type=None, skp_cost=0, faction="NEUTRAL"):
        self.name = name
        self.card_type = card_type
        self.effect = effect
        self.attribute = attribute
        self.image_path = image_path
        self.level = level
        self.faith_points = faith_points
        self.divinity_points = divinity_points
        self.scripture_type = scripture_type
        self.miracle_type = miracle_type
        self.skp_cost = skp_cost
        self.faction = faction
        self.position = None
        self.is_destroyed = False
        self.is_face_down = False
        self.is_selected = False
        
        # Initialize surface and rect
        self.surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.surface.get_rect()
        
        # Load card image if provided
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        else:
            self.image = None
        
    def draw(self, surface):
        """Draw the card on the given surface"""
        # Create background
        if self.is_face_down:
            # Draw face-down card
            pygame.draw.rect(surface, DARK_BLUE, self.rect)
            pygame.draw.rect(surface, GOLD, self.rect, 2)
        else:
            # Draw card background
            pygame.draw.rect(surface, WHITE, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 2)
            
            # Draw card image or details
            if self.image:
                surface.blit(self.image, self.rect)
            else:
                # Draw card details
                font = pygame.font.Font(None, 20)
                
                # Name
                name_text = font.render(self.name, True, BLACK)
                surface.blit(name_text, (self.rect.x + 5, self.rect.y + 5))
                
                # Type
                type_text = font.render(str(self.card_type.value), True, BLACK)
                surface.blit(type_text, (self.rect.x + 5, self.rect.y + 25))
                
        if self.is_selected:
            pygame.draw.rect(surface, GOLD, self.rect, 4)

def create_damage_boost_effect(amount: int) -> Effect:
    return Effect(
        name="Damage Boost",
        timing=Timing.ON_ATTACK,
        condition=lambda state: True,
        action=lambda state: setattr(
            state.current_attack,
            "damage",
            state.current_attack.damage + amount
        )
    )

def create_damage_reduction_effect(amount: int) -> Effect:
    return Effect(
        name="Damage Reduction",
        timing=Timing.ON_DEFEND,
        condition=lambda state: True,
        action=lambda state: setattr(
            state.current_attack,
            "damage",
            state.current_attack.damage - amount
        )
    )