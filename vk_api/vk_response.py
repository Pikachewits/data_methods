import requests
import json
from pprint import pprint

token = '******'
user_id = '******'
method = 'groups.get'

vk_groups = requests.get(f'https://api.vk.com/method/{method}?user_id={user_id}&v=5.130&access_token={token}').json()
# pprint(vk_groups)

group_list=[]

for group in vk_groups['response']['items']:
    group_list.append(group)

pprint(group_list)

with open('group_list.json', 'w') as file:
    json.dump(group_list, file)
