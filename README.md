# Word memorization application for YDSA+

Free Project to memorize words for YDSA+

## API Endpoints

Here are the currently supported API Endpoints.  

| HTTP Verb | Scope                 | Semantic                                           | URL                                |
|-----------|-----------------------|----------------------------------------------------|------------------------------------|
| GET       | Collection of English | Retrieve all English in the collection             | /api/en/words/                     |
| GET       | English               | Retrieve a single English                          | /api/en/words/{word}/              |
| POST      | Collection of English | Create a new English in the collection             | /api/en/words/                     |
| PUT       | English               | Update an existing English                         | /api/en/words/{word}/              |
| ~~PATCH~~ | English               | Partially update an existing English               | /api/en/words/{word}/              |
| DELETE    | English               | Delete an existing English                         | /api/en/words/{word}/              |
| GET       | Collection of Turkish | Retrieve a collection of Turkish from translations | /api/en/words/{word}/translations/ |
| POST      | Collection of Turkish | Append a collection of Turkish from translations   | /api/en/words/{word}/translations/ |
| DELETE    | Collection of Turkish | Remove a collection of Turkish from translations   | /api/en/words/{word}/translations/ |
| GET       | Collection of English | Retrieve a collection of English from synonyms     | /api/en/words/{word}/synonyms/     |
| POST      | Collection of English | Append a collection of English from synonyms       | /api/en/words/{word}/synonyms/     |
| DELETE    | Collection of Turkish | Remove a collection of Turkish from synonyms       | /api/en/words/{word}/synonyms/     |
| GET       | Collection of Game    | Retrieve all Games in the collection               | /api/en/games/                     |
| GET       | Game                  | Retrieve a single Game                             | /api/en/games/{game_name}/         |
| GET       | Game                  | Retrieve a single Game to play                     | /api/en/games/{game_name}/start/   |
| POST      | Game                  | Update or Create a Score in the collection         | /api/en/games/{game_name}/start/   |
| GET       | Collection of WordBox | Retrieve WordBox in the collection                 | /api/en/wordboxes/                 |
| POST      | Collection of WordBox | Create a new WordBox in the collection             | /api/en/wordboxes/                 |
| GET       | WordBox               | Retrieve a single WordBox                          | /api/en/wordboxes/{int:pk}/        |
| PUT       | WordBox               | Update a single WordBox                            | /api/en/wordboxes/{int:pk}/        |
| DELETE    | WordBox               | Delete a single WordBox                            | /api/en/wordboxes/{int:pk}/        |
| GET       | WordBox               | Start a new Game play for single WordBox           | /api/en/wordboxes/{int:pk}/start/  |
| POST      | WordBox               | Update or Create Score in the collection           | /api/en/wordboxes/{int:pk}/start/  |
| GET       | Collection of English | Retrieve a collection of word in WordBox           | /api/en/wordboxes/{int:pk}/words/  |
| POST      | Collection of English | Append a collection of word in the WordBox         | /api/en/wordboxes/{int:pk}/words/  |
| DELETE    | Collection of English | Remove a collection of word in the WordBox         | /api/en/wordboxes/{int:pk}/words/  |
| GET       | Collection of User    | Retrieve a collection of user in WordBox           | /api/en/wordboxes/{int:pk}/users/  |
| POST      | Collection of User    | Append a collection of user in the WordBox         | /api/en/wordboxes/{int:pk}/users/  |
| DELETE    | Collection of User    | Remove a collection of user in the WordBox         | /api/en/wordboxes/{int:pk}/users/  |

## Getting Started
UML:
![UML DIAGRAM](ydsa_uml.jpg)

## Who need this project?

Anyone who want to be the champion of the exam.