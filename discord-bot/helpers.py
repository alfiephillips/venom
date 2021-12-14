import os

def check_env():
    _vars = ["TOKEN", "MONGO_URI", "SERVER_ID"]
    for var in _vars:
        if var not in os.environ:
            print("Missing environment variables!")