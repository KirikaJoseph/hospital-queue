import sys
import os

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ui import launch_app  # Import the function to launch the app

if __name__ == "__main__":
    launch_app()  # Start the application
