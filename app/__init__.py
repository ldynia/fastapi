import os
import sys

# Add to app module to system PATH to avoid circular imports
file_path = os.path.abspath(__file__)
dir_name = os.path.dirname(file_path)
sys.path.append(dir_name)