import json

from flask import Flask
from mongoeng import Workers


def test():
    app = Flask(__name__)
    Workers(app)
    client = app.test_client()
    url = '/user/'

    mock_request_headers = {}

    mock_request_data = {
        'Names': 'rahul',
        'Work': 'carpenter',
        'WorkerId': '453'
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200