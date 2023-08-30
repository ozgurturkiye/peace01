import os
import json

import requests


s = requests.Session()
# username = input("Username: ")
# password = input("Password: ")
username, password = "ozgur", 123

s.auth = (username, password)


def check_connection():
    # Check connection
    r = s.get("http://127.0.0.1:8000/api/login-test-page/")
    if r.status_code == 200:
        print("Successfully connected...")
        print("*** Welcome To Word Memorizing Game ***")
    else:
        print("Connection Fail! Check your username and password.")
        exit()


check_connection()

# Enumerate choices
choices = (
    "Retrieve all words",
    "Create a new word",
    "Retrieve a single word",
    "Update an existing word",
    "Delete an existing word",
    "Play Single Word Game",
    "Retrieve all WordBoxes",
    "Create a new WordBox",
    "Retrieve a single WordBox",
)
message = "Please select what you want?\n"
for index, value in enumerate(choices, start=1):
    message += f"{index} - {value}\n"
message += "Q - Quit\n Make your choice...\n"


def word_many_to_many(base_url, method):
    if method == s.get:
        r = method(base_url)
        print(r)
        print(json.dumps(r.json(), indent=2))
        return

    words = input("Enter comma separated words: ")
    words = words.split(",")
    payload = {"words": words}
    r = method(base_url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))


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
        choice = input(
            """
            1 - Retrieve a collection of Turkish from translations
            2 - Append a collection of Turkish from translations
            3 - Remove a collection of Turkish from translations
            4 - Retrieve a collection of English from synonyms
            5 - Append a collection of English from synonyms
            6 - Remove a collection of Turkish from synonyms
            Please select choices\n
            """
        )
        url_translations = url + "translations/"
        url_synonyms = url + "synonyms/"

        if choice == "1":
            word_many_to_many(url_translations, s.get)
        elif choice == "2":
            word_many_to_many(url_translations, s.post)
        elif choice == "3":
            word_many_to_many(url_translations, s.post)
        elif choice == "4":
            word_many_to_many(url_synonyms, s.get)
        elif choice == "5":
            word_many_to_many(url_synonyms, s.post)
        elif choice == "6":
            word_many_to_many(url_synonyms, s.post)

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
    elif choice == "6":
        url = "http://127.0.0.1:8000/api/en/games/single-word/start/"
        r = s.get(url)
        print(r, r.json())
        print("If you want quit enter Q or q!")
        while True:
            english = r.json().get("english")
            answer = input(f"{english}: ")
            if answer in ("Q", "q"):
                break
            elif answer == "":
                continue
            payload = {"english": english, "turkish": answer}
            r = s.post(url, json=payload)
            print(r, r.json())
    elif choice == "7":
        url = "http://127.0.0.1:8000/api/en/wordboxes/"
        r = s.get(url)
        print(json.dumps(r.json(), indent=2))
        input("Press enter to continue...")

    elif choice == "Q" or choice == "q":
        break
