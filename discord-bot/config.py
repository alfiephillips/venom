# Imports

import os
import dotenv

dotenv.load_dotenv()

# Global variables

TOKEN = os.environ["TOKEN"]
MONGO_URI = os.environ["MONGO_URI"]
SERVER_ID = os.environ["SERVER_ID"]