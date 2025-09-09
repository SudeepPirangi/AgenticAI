"""Common utility file for all the necessary imports"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# print("\nDirectory", parent_dir)

# Now import your module from the parent directory
from constants import AI

from ai.perplexity import Perplexity
from ai.gemini import Gemini


load_dotenv(override=True)

PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_URL = AI["PERPLEXITY"]["BASE_URL"]
PERPLEXITY_MODEL = AI["PERPLEXITY"]["MODEL"]

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = AI["GEMINI"]["BASE_URL"]
GEMINI_MODEL = AI["GEMINI"]["MODEL"]

# Perplexity
perplexity_ai = Perplexity()

# Gemini
gemini_ai = Gemini()
