#! venv/bin/python3
import requests # requires requests library - pip3 install requests
from requests.auth import HTTPDigestAuth

if __name__ == '__main__':
    auth = HTTPDigestAuth('learner', 'p@ssword') # define digest auth info
    token = requests.post('http://localhost:5000/auth/tokens', auth=auth) # get new token
    t_auth_headers = {"Authorization": f"Bearer {token.text}"} # create request header with the new token
    book = {"id": "0000012345", "title": "Lorem Ipsum", "genre": "fantasy", "blurb": "Lorem ipsum, dolor sic amet..."}
    requests.post('http://localhost:5000/api/books', json=book, headers=t_auth_headers) # make post request with token header
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
