import app from mongoeng
import pytest

def test_welcome():
  client = app.test_client()
  url = '/'
  response = client.get(url)
  assert response.get_data() == b'Welcome'

def test_welcome2():
  client = app.test_client()
  url = '/'
  response = client.get(url)
  assert response.status_code == 200 

def test_get():
    client  = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.get_data() 

def test_post():
    client = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.status_code==200    

def test_put():
    client = app.test_client()
    url = '/user/634f246af10b5f16704aa3cf/'
    response = client.get(url)
    assert response.status_code==404

def test_del():
    client = app.test_client()
    url = '/user/634d2edb52df5a21b906aeb9/d'
    response = client.get(url)
    assert response.status_code==405         