import requests

token = '' # Токен учителя или студента курса
response = requests.get(f'http://127.0.0.1:8000/api/v0/courses/1/', headers={'Authorization': f'Token {token}'})
print(response.status_code)