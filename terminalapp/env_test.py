# Rename `os.environ` to `env` for nicer code
from os import environ as env

# pip install python-dotenv
# from dotenv import load_dotenv
# load_dotenv()

print("API_KEY:  {}".format(env["API_KEY"]))
print("HOSTNAME: {}".format(env["HOSTNAME"]))
print("PORT:     {}".format(env["PORT"]))
