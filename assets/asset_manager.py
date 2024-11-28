class CardAssetManager:
    def __init__(self):
        self.image_generator = CardImageGenerator()
        self.card_cache = {}
        
    def get_card_image(self, card_id: str, card_data: Dict) -> pygame.Surface:
        """Get card image, generate placeholder if no art exists"""
        if card_id in self.card_cache:
            return self.card_cache[card_id]
            
        try:
            # Try to load actual card art
            image = pygame.image.load(f"assets/cards/images/{card_id}.png")
        except:
            # Generate placeholder if no art exists
            image = self.image_generator.generate_placeholder_image(card_data)
            
        self.card_cache[card_id] = image
        return image