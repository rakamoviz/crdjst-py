0. Have pyenv
1. Have pyenv-virtualenv https://github.com/pyenv/pyenv-virtualenv installed
2. pyenv virtualenv 3.7.3 crdjst-py
3. pip install -r requirements.txt 
4. export $(cat .env | xargs)