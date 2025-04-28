"""
Setup script for Commit Analysis Agent.
"""

import os
import subprocess
import sys
from pathlib import Path

def setup_project():
    """Set up the project environment."""
    
    print("Setting up Commit Analysis Agent...")
    
    # Create necessary directories
    directories = [
        'data',
        'data/embeddings',
        'logs',
        'reports'
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
    
    # Create virtual environment if it doesn't exist
    if not Path('venv').exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    # Install dependencies
    print("Installing dependencies...")
    pip_path = 'venv/bin/pip' if os.name != 'nt' else 'venv\\Scripts\\pip'
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    
    # Create default configuration
    config = {
        'model_name': 'claude-3-opus-20240229',
        'storage_path': './data',
        'log_level': 'INFO',
        'max_optimization_iterations': 3
    }
    
    with open('config.json', 'w') as f:
        import json
        json.dump(config, f, indent=2)
    
    print("Setup complete! To start the application:")
    print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Run the API server: python src/api_server.py")
    print("3. Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    setup_project()
