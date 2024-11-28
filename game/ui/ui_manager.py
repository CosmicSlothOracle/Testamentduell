import pygame
from typing import Optional, Tuple, Dict, List
from ..card import Card
from ..types import Phase, CardType
from .tooltip import Tooltip, TooltipStyle
from .visual_effects import VisualFeedbackManager, EffectType
from .card_animator import CardAnimator
from .menu import GameMenu

class UIManager:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        
        # Initialize UI components
        self.tooltip = Tooltip(screen, game.debug_font)
        self.visual_feedback = VisualFeedbackManager(screen)
        self.card_animator = CardAnimator()
        
        # Mouse state
        self.dragging_card = None
        self.hover_card = None
        self.selected_card = None
        self.drag_start_pos = None
        
        # UI state
        self.valid_zones = []
        
        self.menu = GameMenu(screen)
        self.action_confirmation = None
        
    def update(self):
        """Update UI state"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update components
        self.visual_feedback.update()
        self.card_animator.update()
        self.tooltip.update()
        
        # Update hover states
        self._update_hover_states(mouse_pos)
        
        # Update drag states
        if self.dragging_card:
            self._update_drag_states(mouse_pos)
            
    def draw(self):
        """Draw UI elements"""
        self.screen.fill((0, 0, 0))  # Clear screen
        self.game.draw()  # Draw game elements
        self.tooltip.draw()
        self.visual_feedback.draw()
        self.card_animator.draw()
        self.menu.draw()
        pygame.display.flip()
        
    def _draw_action_buttons(self):
        """Draw available action buttons"""
        available_actions = self.game.get_available_actions()
        
        for action, rect in self.game.action_buttons.items():
            if action in available_actions:
                color = (100, 100, 100)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    color = (120, 120, 120)
                    
                pygame.draw.rect(self.screen, color, rect)
                text = self.game.debug_font.render(action, True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
                
    def _draw_phase_indicator(self):
        """Draw current phase indicator"""
        phase_text = f"Phase: {self.game.current_phase.value}"
        text = self.game.debug_font.render(phase_text, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
    def show_phase_change(self, new_phase: Phase):
        """Show phase change animation"""
        self.visual_feedback.add_effect(
            "phase_change",
            EffectType.FADE,
            color=(100, 200, 255),
            duration=30
        )
        
        self.tooltip.show(
            (self.screen.get_width() // 2, 100),
            [f"Entering {new_phase.value} Phase"],
            style=TooltipStyle.ACTION,
            duration=60
        )
        
    def show_turn_change(self, new_player_index: int):
        """Show turn change animation"""
        self.visual_feedback.add_effect(
            "turn_change",
            EffectType.FLASH,
            color=(255, 200, 100),
            duration=45
        )
        
        self.tooltip.show(
            (self.screen.get_width() // 2, 100),
            [f"Player {new_player_index + 1}'s Turn"],
            style=TooltipStyle.ACTION,
            duration=60
        )
        
    def handle_event(self, event):
        """Handle UI events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left release
                return self._handle_left_release(event.pos)
                
        elif event.type == pygame.MOUSEMOTION:
            return self._handle_mouse_motion(event.pos)
            
    def _handle_left_click(self, pos):
        """Handle left mouse button click"""
        # Check action buttons first
        for action, rect in self.game.action_buttons.items():
            if rect.collidepoint(pos) and action in self.game.get_available_actions():
                return {"action": action}
                
        # Check if clicking a card in hand
        card = self._get_card_at_position(pos)
        if card:
            self.dragging_card = card
            self.drag_start_pos = pos
            return {"action": "card_selected", "card": card}
            
        return None
        
    def _handle_right_click(self):
        """Handle right click"""
        if self.dragging_card:
            self.dragging_card = None
            return {"action": "cancel_action"}
        return None
        
    def _handle_left_release(self, pos):
        """Handle left mouse button release"""
        if self.dragging_card:
            zone = self._get_zone_at_position(pos)
            if zone in self.valid_zones:
                action = {
                    "action": "play_card",
                    "card": self.dragging_card,
                    "zone": zone
                }
                self.dragging_card = None
                return action
                
        self.dragging_card = None
        return None
        
    def _handle_mouse_motion(self, pos):
        """Handle mouse motion"""
        # Update hover card
        prev_hover = self.hover_card
        self.hover_card = self._get_card_at_position(pos)
        
        if self.hover_card != prev_hover:
            return {"action": "hover_change", "card": self.hover_card}
            
        return None
        
    def _get_card_at_position(self, pos) -> Optional[Card]:
        """Get card at the given position"""
        current_player = self.game.players[self.game.active_player_index]
        
        # Check hand
        for card in current_player.hand:
            if hasattr(card, 'rect') and card.rect.collidepoint(pos):
                return card
                
        # Check sanctuary
        for card in current_player.sanctuary:
            if hasattr(card, 'rect') and card.rect.collidepoint(pos):
                return card
                
        return None
        
    def _get_zone_at_position(self, pos) -> Optional[str]:
        """Get zone at the given position"""
        for zone_name, zone_data in self.game.zones.items():
            if zone_data["rect"].collidepoint(pos):
                return zone_name
        return None
        
    def _get_card_tooltip_text(self, card) -> List[str]:
        """Get tooltip text for card"""
        lines = [
            card.name,
            f"Type: {card.card_type.value}",
            f"SKP Cost: {card.skp_cost}"
        ]
        
        if hasattr(card, 'faith_points'):
            lines.append(f"Faith Points: {card.faith_points}")
        if hasattr(card, 'divinity_points'):
            lines.append(f"Divinity Points: {card.divinity_points}")
        if hasattr(card, 'effect') and card.effect:
            lines.append(f"Effect: {card.effect}")
            
        return lines
        
    def _update_valid_zones(self):
        """Update which zones are valid for the currently selected card"""
        self.valid_zones = []
        
        if not self.dragging_card:
            return
            
        current_player = self.game.players[self.game.active_player_index]
        
        # Check if card can be played based on current phase
        if self.game.current_phase == Phase.PREPARATION:
            # Check sanctuary placement
            if (self.dragging_card.card_type in [CardType.BELIEVER, CardType.RELIC] and
                len(current_player.sanctuary) < MAX_SANCTUARY_SIZE and
                current_player.current_skp >= self.dragging_card.skp_cost):
                self.valid_zones.append(f"SANCTUARY_P{self.game.active_player_index + 1}")
        
    def _update_hover_states(self, mouse_pos):
        """Update all hover states"""
        # Update card hover
        prev_hover = self.hover_card
        self.hover_card = self._get_card_at_position(mouse_pos)
        
        if self.hover_card != prev_hover:
            if self.hover_card:
                self.tooltip.show(
                    mouse_pos,
                    self._get_card_tooltip_text(self.hover_card),
                    style=TooltipStyle.CARD
                )
            else:
                self.tooltip.hide()
                
        # Update zone hover
        self.hover_zone = self._get_zone_at_position(mouse_pos)
        if self.hover_zone:
            zone_data = self.game.zones[self.hover_zone]
            self.visual_feedback.add_effect(
                f"zone_{self.hover_zone}",
                EffectType.HIGHLIGHT,
                color=(150, 150, 150)
            )
            
    def _update_drag_states(self, mouse_pos):
        """Update drag-related states"""
        if self.dragging_card:
            self.dragging_card.rect.center = mouse_pos
            self._update_valid_zones()
            
    def _highlight_zone(self, zone):
        """Highlight zone"""
        # Implement highlighting zone logic here
        pass
        
    def _draw_dragged_card(self):
        """Draw card being dragged"""
        if self.dragging_card:
            mouse_pos = pygame.mouse.get_pos()
            self.dragging_card.draw(
                self.screen,
                mouse_pos[0] - self.dragging_card.rect.width // 2,
                mouse_pos[1] - self.dragging_card.rect.height // 2
            ) 
        
    def handle_click(self, pos):
        # Check menu first
        menu_action = self.menu.handle_click(pos)
        if menu_action:
            return self._handle_menu_action(menu_action)
            
        # Handle confirmation button if visible
        if self.action_confirmation and self.action_confirmation['button'].collidepoint(pos):
            return self._handle_confirmation()
            
        # Handle card selection
        clicked_card = self._get_card_at_position(pos)
        if clicked_card:
            self.selected_card = clicked_card
            self._show_valid_zones()
            return
            
        # Handle zone selection if card is selected
        if self.selected_card:
            zone = self._get_zone_at_position(pos)
            if zone in self.valid_zones:
                self._show_confirmation(zone) 