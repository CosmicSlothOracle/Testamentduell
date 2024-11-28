import os
import sys
import argparse
from pathlib import Path

# Add the parent directory to Python path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.card_import_system import CardImportSystem

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Import cards from spreadsheet')
    parser.add_argument('--file', '-f', 
                       default=os.path.join("assets", "card_data.xlsx"),
                       help='Path to the card data spreadsheet')
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='Enable verbose output')
    args = parser.parse_args()

    # Initialize the import system
    importer = CardImportSystem()
    
    # Convert to Path object for better path handling
    spreadsheet_path = Path(args.file)
    
    try:
        if args.verbose:
            print(f"Starting import from: {spreadsheet_path}")
            
        # Run the import
        result = importer.import_spreadsheet(spreadsheet_path)
        
        if args.verbose:
            print(f"Successfully imported {result.card_count} cards")
            
    except FileNotFoundError:
        print(f"Error: Could not find spreadsheet at {spreadsheet_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during import: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()