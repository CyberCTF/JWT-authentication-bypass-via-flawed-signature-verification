#!/usr/bin/env python3
"""
Build script for Corporate Asset Management System
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        return False
    
    print("✅ Python version check passed")
    
    # Check Docker
    if not run_command("docker --version"):
        print("⚠️  Docker not found - manual installation will be required")
    else:
        print("✅ Docker found")
    
    # Check Docker Compose
    if not run_command("docker-compose --version"):
        print("⚠️  Docker Compose not found - using docker compose instead")
    else:
        print("✅ Docker Compose found")
    
    return True

def setup_virtual_environment():
    """Setup Python virtual environment"""
    print("🐍 Setting up Python virtual environment...")
    
    if not run_command("python -m venv venv"):
        print("❌ Failed to create virtual environment")
        return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = ".\\venv\\Scripts\\activate && pip install -r build\\requirements.txt"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate && pip install -r build/requirements.txt"
    
    if not run_command(activate_cmd):
        print("❌ Failed to install dependencies")
        return False
    
    print("✅ Virtual environment setup complete")
    return True

def initialize_database():
    """Initialize SQLite database with sample data"""
    print("🗄️  Initializing database...")
    
    db_path = Path("build/corporate_assets.db")
    
    # Remove existing database if it exists
    if db_path.exists():
        db_path.unlink()
    
    # Run the Flask app initialization
    if not run_command("python app.py --init-db", cwd="build"):
        print("⚠️  Database initialization via app failed, trying manual setup...")
        
        # Manual database setup
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Create tables and insert data (simplified version)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'employee',
                    department TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute("INSERT OR IGNORE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                          ('mitchell.parker', 'asset2024!', 'employee', 'IT Support'))
            cursor.execute("INSERT OR IGNORE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                          ('admin', 'admin_pass_2024', 'admin', 'Management'))
            
            conn.commit()
            conn.close()
            print("✅ Database initialized manually")
        except Exception as e:
            print(f"❌ Manual database initialization failed: {e}")
            return False
    else:
        print("✅ Database initialized via application")
    
    return True

def build_docker_image():
    """Build Docker image"""
    print("🐳 Building Docker image...")
    
    if not run_command("docker build -t corporate-assets -f deploy/Dockerfile ."):
        print("❌ Failed to build Docker image")
        return False
    
    print("✅ Docker image built successfully")
    return True

def run_tests():
    """Run test suite"""
    print("🧪 Running tests...")
    
    # Install test dependencies
    test_deps = "pip install pytest requests"
    if not run_command(test_deps):
        print("❌ Failed to install test dependencies")
        return False
    
    # Run tests
    if not run_command("python -m pytest test_app.py -v", cwd="test"):
        print("❌ Tests failed")
        return False
    
    print("✅ All tests passed")
    return True

def create_build_info():
    """Create build information file"""
    print("📝 Creating build information...")
    
    import datetime
    
    build_info = f"""# Build Information

**Build Date:** {datetime.datetime.now().isoformat()}
**Python Version:** {sys.version}
**Build System:** {os.name}

## Components Built

- ✅ Flask Application
- ✅ SQLite Database
- ✅ Docker Image
- ✅ Test Suite
- ✅ Documentation

## Next Steps

1. Run the application:
   ```bash
   docker-compose -f deploy/docker-compose.yml up
   ```

2. Access the application:
   ```
   http://localhost:3206
   ```

3. Login credentials:
   - Employee: mitchell.parker / asset2024!
   - Admin: admin / admin_pass_2024

## Security Note

This application contains a deliberate JWT vulnerability for educational purposes.
Do not use in production without proper security fixes.
"""
    
    with open("build_info.md", "w") as f:
        f.write(build_info)
    
    print("✅ Build information created")
    return True

def main():
    """Main build process"""
    print("🚀 Corporate Asset Management System - Build Process")
    print("=" * 60)
    
    # Change to project root directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    steps = [
        ("Checking dependencies", check_dependencies),
        ("Setting up virtual environment", setup_virtual_environment),
        ("Initializing database", initialize_database),
        ("Building Docker image", build_docker_image),
        ("Running tests", run_tests),
        ("Creating build information", create_build_info),
    ]
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if not step_function():
            print(f"❌ Build failed at step: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 BUILD SUCCESSFUL!")
    print("✅ Corporate Asset Management System is ready to deploy")
    print("\n📋 Quick Start:")
    print("   docker-compose -f deploy/docker-compose.yml up")
    print("   Open: http://localhost:3206")
    print("\n🔐 Default credentials:")
    print("   Employee: mitchell.parker / asset2024!")
    print("   Admin: admin / admin_pass_2024")

if __name__ == "__main__":
    main()
