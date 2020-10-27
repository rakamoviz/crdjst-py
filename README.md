0. Have pyenv
1. Have pyenv-virtualenv https://github.com/pyenv/pyenv-virtualenv installed
2. pyenv virtualenv 3.7.3 crdjst-py
3. pip install -r requirements.txt 
4. export $(cat .env | xargs)
5. curl -X POST -v --header "Content-Type: application/json"  http://127.0.0.1:5000/auth --data '{"username":"user1","password":"password"}'
6. curl -v http://127.0.0.1:5000/rates?date=2020-10-20T12:00:00-05:00 --header "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDM4MzIyNzYsImlhdCI6MTYwMzgzMTk3NiwibmJmIjoxNjAzODMxOTc2LCJpZGVudGl0eSI6MX0.oJco70C0Akj0VBwVe4ZzVxvZw0zv5OcuemeXN8aC3p8"