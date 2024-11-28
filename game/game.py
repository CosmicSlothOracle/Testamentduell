import pygame
import json
from pathlib import Path
from .core.player import Player
from .core.card import Card
from .core.combat import CombatManager
from .ui.ui_manager import UIManager
from .constants import *
from .types import Position, CardType, Phase

class TestamentDuelGame:
    def __init__(self, screen, clock, debug=False):
        self.screen = screen
        self.clock = clock
        self.debug = debug
        
        # Initialize managers
        self.ui_manager = UIManager(screen, self)
        self.combat_manager = CombatManager()
        
        # Load decks from JSON
        player1_deck = self._load_deck("assets/decks/player1_deck.json")
        player2_deck = self._load_deck("assets/decks/player2_deck.json")
        
        # Initialize players with proper decks
        self.players = [
            Player("Player 1", player1_deck),
            Player("Player 2", player2_deck)
        ]
        
        # Game state
        self.current_phase = Phase.INVOCATION
        self.active_player_index = 0
        self.turn_count = 1
        self.game_over = False
        
        # Draw starting hands
        for player in self.players:
            for _ in range(5):
                player.draw_card()
                
    def _load_deck(self, filepath: str) -> list:
        """Load deck from JSON file"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Deck file not found: {filepath}")
            
        with open(path) as f:
            deck_data = json.load(f)
            
        deck = []
        for card_data in deck_data:
            card = Card(
                name=card_data["name"],
                card_type=CardType[card_data["card_type"]],
                effect=card_data["effect"],
                faith_points=card_data.get("faith_points"),
                divinity_points=card_data.get("divinity_points"),
                skp_cost=card_data["skp_cost"]
            )
            deck.append(card)
        return deck

    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            self._handle_key_press(event)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
            
        return True
        
    def _handle_key_press(self, event):
        """Handle keyboard controls"""
        if self.game_over:
            return
            
        current_player = self.players[self.active_player_index]
        
        if event.key == pygame.K_SPACE:  # Draw card
            if self.current_phase == Phase.INVOCATION:
                current_player.draw_card()
                self._advance_phase()
                
        elif event.key == pygame.K_TAB:  # End phase
            self._advance_phase()
            
        elif event.key == pygame.K_RETURN:  # End turn
            self._end_turn()
            
    def _handle_mouse_click(self, event):
        """Handle mouse interactions"""
        if self.game_over:
            return
            
        if event.button == 1:  # Left click
            pos = pygame.mouse.get_pos()
            result = self.ui_manager.handle_click(pos)
            
            if result:
                if result.get("action") == "card_selected":
                    self._handle_card_selection(result["card"])
                elif result.get("action") in self.phase_actions[self.current_phase]:
                    self.handle_action(result["action"])
                    
        elif event.button == 3:  # Right click
            self._handle_right_click(event.pos)

    def _handle_card_selection(self, card):
        """Handle card selection logic"""
        current_player = self.players[self.active_player_index]
        
        if self.current_phase == Phase.PREPARATION:
            # Handle playing cards to zones
            if card in current_player.hand:
                valid_zones = self._get_valid_zones(card)
                self.ui_manager.show_zone_selection(valid_zones)
                
        elif self.current_phase == Phase.SUMMONING:
            # Handle summoning believers
            if card.card_type == CardType.BELIEVER and card in current_player.hand:
                if current_player.current_skp >= card.skp_cost:
                    if len(current_player.sanctuary) < MAX_SANCTUARY_SIZE:
                        self._summon_believer(card)
                        
        elif self.current_phase == Phase.MISSION:
            # Handle mission assignments
            if card in current_player.sanctuary:
                self._assign_mission(card)

    def _handle_right_click(self, pos):
        """Handle right click for card detail view"""
        card = self.ui_manager.get_card_at_position(pos)
        if card:
            self.ui_manager.show_card_detail(card)

    def _get_valid_zones(self, card) -> list:
        """Get valid zones for playing a card"""
        valid_zones = []
        
        if card.card_type == CardType.BELIEVER:
            valid_zones.append("SANCTUARY")
        elif card.card_type == CardType.RELIC:
            if self.players[self.active_player_index].sanctuary:
                valid_zones.append("SANCTUARY")
        elif card.card_type in [CardType.MIRACLE, CardType.MISSION]:
            valid_zones.append("MISSION")
            
        return valid_zones

    def _summon_believer(self, card):
        """Handle believer summoning"""
        current_player = self.players[self.active_player_index]
        card_index = current_player.hand.index(card)
        
        if current_player.play_card(card_index, "SANCTUARY"):
            self.ui_manager.show_message(f"Summoned {card.name}")
            return True
        return False

    def update(self):
        """Update game state"""
        if not self.game_over:
            self.ui_manager.update()
            self._check_win_condition()
            
    def _check_win_condition(self):
        """Check if game is over"""
        for i, player in enumerate(self.players):
            if player.grace_points <= 0:
                self.game_over = True
                print(f"Game Over! {self.players[1-i].name} wins!")
                break
                
            if len(player.deck) == 0 and len(player.hand) == 0:
                self.game_over = True
                print(f"Game Over! {self.players[1-i].name} wins by deck out!")
                break
                
    def draw(self):
        """Draw game state"""
        self.screen.fill((50, 50, 50))  # Dark gray background
        self.ui_manager.draw()
        
        if self.game_over:
            self._draw_game_over()
            
        if self.debug:
            self._draw_debug_info()
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False
                    break
                    
            self.update()
            self.draw()
            self.clock.tick(60)
            
        return 0
