import uuid

import requests
import json
from requests.auth import HTTPBasicAuth

CLIENT_ID = '56e50044-520d-4630-b002-5311870c278a'
SECRET = 'NTZlNTAwNDQtNTIwZC00NjMwLWIwMDItNTMxMTg3MGMyNzhhOjVkNzM3OTk3LWEyMTAtNGM4My04ZDgzLWM5MWFhODdkMjI1MA=='

# curl -L -X POST 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth' \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -H 'Accept: application/json' \
# -H 'RqUID: <идентификатор_запроса>' \
# -H 'Authorization: Basic ключ_авторизации' \
# --data-urlencode 'scope=GIGACHAT_API_PERS'

def get_access_token() -> str:
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {SECRET}'
    }
    payload = {'scope': 'GIGACHAT_API_PERS'}
    res = requests.post(url=url,
                        headers=headers,
                        data=payload,
                        verify=False)
    access_token = res.json()['access_token']
    return access_token


def get_image():
    pass

def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": msg
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url=url, headers=headers, data=payload, verify=False)

    return response.json()['choices'][0]['message']['content']

def send_prompt_and_get_response():
    pass