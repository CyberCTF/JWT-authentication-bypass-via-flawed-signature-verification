#!/usr/bin/env python3
"""
Initialization script for Corporate Asset Management System
Creates the database and sets up initial data
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the Flask app
from app import init_db

def main():
    """Initialize the application database"""
    print("🗄️  Initializing Corporate Asset Management System database...")
    
    try:
        init_db()
        print("✅ Database initialized successfully!")
        print("📋 Default accounts created:")
        print("   Employee: mitchell.parker / asset2024!")
        print("   Employee: sarah.johnson / secure789")  
        print("   Admin: admin / admin_pass_2024")
        print("🎯 Flag location: Admin Panel > Classified Information")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
