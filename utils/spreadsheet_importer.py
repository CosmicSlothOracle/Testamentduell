import pandas as pd
import json
from typing import Dict

class CardImporter:
    def __init__(self):
        self.database_path = "src/assets/cards/card_database.json"
        
    def import_from_spreadsheet(self, spreadsheet_path: str):
        """Import card data from spreadsheet"""
        # Read spreadsheet
        df = pd.read_excel(spreadsheet_path)  # or pd.read_csv for CSV files
        
        # Load existing database
        with open(self.database_path, 'r') as f:
            database = json.load(f)
            
        # Process each card
        for _, row in df.iterrows():
            card_data = self._process_card_row(row)
            set_code = card_data.pop('set_code')
            card_id = card_data.pop('card_id')
            
            # Add to appropriate set
            if set_code in database['card_sets']:
                database['card_sets'][set_code]['cards'][card_id] = card_data
            
        # Save updated database
        with open(self.database_path, 'w') as f:
            json.dump(database, f, indent=4)
    
    def _process_card_row(self, row: pd.Series) -> Dict:
        """Convert spreadsheet row to card data"""
        return {
            'card_id': row['ID'],
            'set_code': row['Set'],
            'name': row['Name'],
            'card_type': row['Type'],
            'attribute': row['Attribute'],
            'effect': row['Effect'],
            'level': row['Level'] if 'Level' in row else None,
            'faith_points': row['Faith Points'] if 'Faith Points' in row else None,
            'divinity_points': row['Divinity Points'] if 'Divinity Points' in row else None,
            'scripture_type': row['Scripture Type'] if 'Scripture Type' in row else None,
            'miracle_type': row['Miracle Type'] if 'Miracle Type' in row else None,
            'skp_cost': row['SKP Cost'],
            'faction': row['Faction'],
            'rarity': row['Rarity'] if 'Rarity' in row else 'Common',
            'flavor_text': row['Flavor Text'] if 'Flavor Text' in row else None
        }