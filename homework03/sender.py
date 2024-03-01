import requests

response = requests.post(
    'http://127.0.0.1:5000/send',
    json={
        'name': 'Nick',
        'text': '123'
    }
)

print(response.text)


