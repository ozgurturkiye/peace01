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
    "Play a Single Word Game",
    "Retrieve all WordBoxes",
    "Create a new WordBox",
    "Retrieve, Update or Delete a WordBox",
    "Play a WordBox Game",
)
message = "Please select what you want?\n"
for index, value in enumerate(choices, start=1):
    message += f"{index} - {value}\n"
message += "Q - Quit\n Make your choice...\n"


def get_word():
    english = input("Word: ")
    url = f"http://127.0.0.1:8000/api/en/words/{english}/"
    r = s.get(url)
    return r


def put_word():
    english = input("Word: ")
    url = f"http://127.0.0.1:8000/api/en/words/{english}/"
    new_english = input("Enter the correct spelling: ")
    payload = {"name": new_english}
    r = s.put(url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))
    input("Press enter to continue...")


def delete_word():
    english = input("Word: ")
    url = f"http://127.0.0.1:8000/api/en/words/{english}/"
    r = s.delete(url)
    print(r)
    input("Press enter to continue...")


def word_many_to_many_get(base_url):
    r = s.get(base_url)
    print(r)
    print(json.dumps(r.json(), indent=2))
    return r


def word_many_to_many_post(base_url):
    words = input("Enter comma separated words: ")
    words = words.split(",")
    payload = {"words": words}
    r = s.post(base_url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))


def word_many_to_many_delete(base_url):
    words = input("Enter comma separated words: ")
    words = words.split(",")
    payload = {"words": words}
    r = s.delete(base_url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))


def get_wordboxes():
    url = "http://127.0.0.1:8000/api/en/wordboxes/"
    r = s.get(url)
    print(json.dumps(r.json(), indent=2))
    input("Press enter to continue...")


def post_wordboxes():
    url = "http://127.0.0.1:8000/api/en/wordboxes/"
    name = input("WordBox name: ")
    payload = {"name": name}
    r = s.post(url, json=payload)
    print(r)
    print(json.dumps(r.json(), indent=2))
    input("Press enter to continue...")


def get_wordbox():
    url = "http://127.0.0.1:8000/api/en/wordboxes/"
    r = s.get(url)
    wordbox_list = r.json()["personal"] + r.json()["friend"]
    print("Choose WordBox You want to work on:")
    for index, value in enumerate(wordbox_list, start=1):
        print(index, value["name"])

    while True:
        try:
            choice = int(input("Choose WordBox Number: ")) - 1
            wordbox = wordbox_list[choice]
            break
        except (ValueError, IndexError) as e:
            print("input must be valid")

    return wordbox


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
        r = get_word()
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
            word_many_to_many_get(url_translations)
        elif choice == "2":
            word_many_to_many_post(url_translations)
        elif choice == "3":
            word_many_to_many_post(url_translations)
        elif choice == "4":
            word_many_to_many_get(url_synonyms)
        elif choice == "5":
            word_many_to_many_post(url_synonyms)
        elif choice == "6":
            word_many_to_many_post(url_synonyms)

        input("Press enter to continue...")
    elif choice == "4":
        put_word()
    elif choice == "5":
        delete_word()
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
        get_wordboxes()
    elif choice == "8":
        post_wordboxes()
    elif choice == "9":
        wordbox = get_wordbox()
        url = f"http://127.0.0.1:8000/api/en/wordboxes/{wordbox['id']}/"
        print(wordbox)

        choice = input(
            """
        1 - Update
        2 - Delete\n"""
        )
        if choice == "1":
            name = input("Enter the correct spelling: ")
            payload = {"name": name}
            r = s.put(url, json=payload)
            print(r)
            print(json.dumps(r.json(), indent=2))
        elif choice == "2":
            r = s.delete(url)
            print(r)

        input("Press enter to continue...")
    elif choice == "10":
        wordbox = get_wordbox()
        url = f"http://127.0.0.1:8000/api/en/wordboxes/{wordbox['id']}/start/"
        print(wordbox)
        r = s.get(url)
        print(r, r.json())
        while True:
            english = r.json().get("english")
            answer = input(f"{english}: ")
            if answer in ("Q", "q"):
                break
            # elif answer == "":
            #     continue
            payload = {"turkish": answer}
            r = s.post(url, json=payload)
            print(r, r.json())

    elif choice == "Q" or choice == "q":
        break
