import json
import os


LIB_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(LIB_PATH)
USER_INI = json.loads((open(os.path.join(
                      PROJECT_PATH, 'settings.json'))).read())
