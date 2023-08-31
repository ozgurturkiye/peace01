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
def prepare_choices():
    choices = (
        "Retrieve all words",
        "Create a new word",
        "Retrieve a single word",
        "Update an existing word",
        "Delete an existing word",
        "Play a Single Word Game",
        "Retrieve all WordBoxes",
        "Create a new WordBox",
        "Retrieve, Update or Delete a WordBox",
        "Play a WordBox Game",
    )
    message = "Please select what you want?\n"
    for index, value in enumerate(choices, start=1):
        message += f"{index} - {value}\n"
    message += "Q - Quit\n Make your choice or Q to quit...\n"
    return message


message = prepare_choices()


def get_word_list():
    url = "http://127.0.0.1:8000/api/en/words/"
    return s.get(url)


def post_word():
    url = "http://127.0.0.1:8000/api/en/words/"
    english = input("Word: ")
    payload = {"name": english}
    return s.post(url, json=payload)


def get_word():
    english = input("Word: ")
    url = f"http://127.0.0.1:8000/api/en/words/{english}/"
    return s.get(url)


def put_word():
    english = input("Word: ")
    url = f"http://127.0.0.1:8000/api/en/words/{english}/"
    new_english = input("Enter the correct spelling: ")
    payload = {"name": new_english}
    return s.put(url, json=payload)


def delete_word():
    english = input("Word: ")
    url = f"http://127.0.0.1:8000/api/en/words/{english}/"
    return s.delete(url)


def get_translations_or_synonyms(base_url):
    r = s.get(base_url)
    print(r)
    print(json.dumps(r.json(), indent=2))


def post_translations_or_synonyms(base_url):
    words = input("Enter comma separated words: ")
    words = words.split(",")
    payload = {"words": words}
    r = s.post(base_url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))


def remove_translations_or_synonyms(base_url):
    words = input("Enter comma separated words: ")
    words = words.split(",")
    payload = {"words": words}
    r = s.delete(base_url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))


def get_wordboxes():
    url = "http://127.0.0.1:8000/api/en/wordboxes/"
    return s.get(url)


def post_wordboxes():
    url = "http://127.0.0.1:8000/api/en/wordboxes/"
    name = input("WordBox name: ")
    payload = {"name": name}
    return s.post(url, json=payload)


def get_wordbox_url():
    r = get_wordboxes()
    wordbox_list = r.json()["personal"] + r.json()["friend"]
    print("Choose WordBox You want to work on:")
    for index, value in enumerate(wordbox_list, start=1):
        print(index, value["name"])

    while True:
        try:
            choice = int(input("Choose WordBox Number: ")) - 1
            wordbox_id = wordbox_list[choice]["id"]
            break
        except (ValueError, IndexError) as e:
            print("input must be valid")

    return f"http://127.0.0.1:8000/api/en/wordboxes/{wordbox_id}/"


# Main loop
while True:
    choice = input(message)

    if choice == "1":
        r = get_word_list()
        print(json.dumps(r.json(), indent=2))
    elif choice == "2":
        while True:
            r = post_word()
            print(r)
            print(json.dumps(r.json(), indent=2))
            choice = input("To add new word press Enter or quit enter Q or q ...")
            if choice == "Q" or choice == "q":
                break
    elif choice == "3":
        r = get_word()
        print(json.dumps(r.json(), indent=2))
        url_translations = r.url + "translations/"
        url_synonyms = r.url + "synonyms/"
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
        if choice == "1":
            get_translations_or_synonyms(url_translations)
        elif choice == "2":
            post_translations_or_synonyms(url_translations)
        elif choice == "3":
            remove_translations_or_synonyms(url_translations)
        elif choice == "4":
            get_translations_or_synonyms(url_synonyms)
        elif choice == "5":
            post_translations_or_synonyms(url_synonyms)
        elif choice == "6":
            remove_translations_or_synonyms(url_synonyms)
    elif choice == "4":
        r = put_word()
        print(r)
        print(json.dumps(r.json(), indent=2))
    elif choice == "5":
        r = delete_word()
        print(r)
    elif choice == "6":
        url = "http://127.0.0.1:8000/api/en/games/single-word/start/"
        r = s.get(url)
        print(r)
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
        r = get_wordboxes()
        print(json.dumps(r.json(), indent=2))
    elif choice == "8":
        r = post_wordboxes()
        print(r)
        print(json.dumps(r.json(), indent=2))
    elif choice == "9":
        url = get_wordbox_url()

        choice = input(
            """
        1 - Get
        2 - Update
        3 - Delete\n"""
        )
        if choice == "1":
            r = s.get(url)
            print(r)
            print(json.dumps(r.json(), indent=2))
        elif choice == "2":
            name = input("Enter the correct spelling: ")
            payload = {"name": name}
            r = s.put(url, json=payload)
            print(r)
            print(json.dumps(r.json(), indent=2))
        elif choice == "3":
            r = s.delete(url)
            print(r)
    elif choice == "10":
        url = get_wordbox_url()
        url += "start/"
        r = s.get(url)
        print(r, r.json())
        while True:
            english = r.json().get("english")
            if english:
                answer = input(f"{english}: ")
            else:
                answer = input("To continue press enter or Quit press Q ")

            if answer in ("Q", "q"):
                break
            payload = {"turkish": answer}
            r = s.post(url, json=payload)
            print(r, r.json())
    elif choice == "Q" or choice == "q":
        break

    input("Press enter to continue...")
