import os
import json

import requests

# Prepare data
url = ""
payload = {}

s = requests.Session()
# username = input("Username: ")
# password = input("Password: ")
username, password = "ozgur", 123

s.auth = (username, password)

# Check connection
r = s.get("http://127.0.0.1:8000/api/login-test-page/")
if r.status_code == 200:
    print("Successfully connected...")
    print("*** Welcome To Word Memorizing Game ***")
else:
    print("Connection Fail! Check your username and password.")
    exit()

choices = (
    "Retrieve all words",
    "Create a new word",
    "Retrieve a single word",
    "Update an existing word",
    "Delete an existing word",
    "Retrieve all games",
    "Retrieve all WordBoxes",
    "Create a new WordBox",
    "Retrieve a single WordBox",
)
message = "Please select what you want?\n"
for number, choice in enumerate(choices, start=1):
    message += f"{number} - {choice}\n"
message += "Q - Quit\n Make your choice...\n"

# Main loop
while True:
    choice = input(message)

    if choice == "1":
        url = "http://127.0.0.1:8000/api/en/words/"
        r = s.get(url)
        print(json.dumps(r.json(), indent=2))
        input("Press enter to continue...")
    elif choice == "2":
        url = "http://127.0.0.1:8000/api/en/words/"
        while True:
            english = input("Word: ")
            payload = {"name": english}
            r = s.post(url, json=payload)
            print(r)
            print(json.dumps(r.json(), indent=2))
            choice = input("To add new word press Enter or quit enter Q or q ...")
            if choice == "Q" or choice == "q":
                break
    elif choice == "3":
        english = input("Word: ")
        url = f"http://127.0.0.1:8000/api/en/words/{english}/"
        r = s.get(url)
        print(r)
        print(json.dumps(r.json(), indent=2))
        input("Press enter to continue...")
    elif choice == "4":
        english = input("Word: ")
        url = f"http://127.0.0.1:8000/api/en/words/{english}/"
        new_english = input("Enter the correct spelling: ")
        payload = {"name": new_english}
        r = s.put(url, json=payload)
        print(r)
        print(json.dumps(r.json(), indent=2))
        input("Press enter to continue...")
    elif choice == "5":
        english = input("Word: ")
        url = f"http://127.0.0.1:8000/api/en/words/{english}/"
        r = s.delete(url)
        print(r)
        input("Press enter to continue...")
    elif choice == "Q" or choice == "q":
        break
