"""Entry point for assistant-bot-G30 CLI"""
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

def run():
    """Run the assistant bot"""
    main()

if __name__ == "__main__":
    run()
