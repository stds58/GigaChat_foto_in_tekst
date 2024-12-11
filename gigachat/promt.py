import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()


TOKEN_GIGACHAT = os.getenv('TOKEN_GIGACHAT')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CERTIFICATE = os.getenv('CERTIFICATE')
relative_path = "certificate/russian_trusted_root_ca.cer"
CERTIFICATE = os.path.abspath(relative_path)

#пользовательские переменные
FOTO_PATH = 'C:\\Users\\valar\\Downloads\\Снимок3.jpeg'
CONTENT =  "Распознай весь текст в этом снимке.Покажи только этот текст в формате json."

def get_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': CLIENT_SECRET,
        'Authorization': f'Basic {TOKEN_GIGACHAT}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=CERTIFICATE)
    return response.json()

access_token = get_token()


url = "https://gigachat.devices.sberbank.ru/api/v1/files"
payload = {'purpose': 'general'}
files=[
('file',('response.jpeg',open(FOTO_PATH,'rb'),'image/jpeg'))
]
headers = {
'Authorization': f'Bearer {access_token.get("access_token")}'
}
response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=CERTIFICATE)
file_id = response.json().get('id')


url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
payload = json.dumps({
  "model": "GigaChat-Pro",
  "messages": [
    {
      "role": "user",
      "content": CONTENT,
      "attachments": [file_id]
    }
  ],
  "stream": False,
  "update_interval": 0
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {access_token.get("access_token")}'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=CERTIFICATE)
print(response.text)
print(response.json().get('choices')[0].get('message').get('content'))



