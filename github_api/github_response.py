import json
import requests


def repo_function(url, user):
    response = requests.get(f'{url}/users/{user}/repos')

    some_list = []
    for i in response.json():
        some_list.append(i['name'])
        print(i['name'])

    with open('repositories.json', 'w') as file:
        json.dump(some_list, file)

    with open('full_response.json', 'w') as file:
        json.dump(response.json(), file)


repo_function('https://api.github.com', 'Pikachewits')