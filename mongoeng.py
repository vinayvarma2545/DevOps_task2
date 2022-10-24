from concurrent.futures.thread import _worker
from pyexpat import model
from urllib import response
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck

app = Flask(__name__)

health = HealthCheck()

app.config['MONGODB_SETTINGS'] = {
  'db': 'Company',
  'host': 'localhost',
  'port': 27017
}

db = MongoEngine()
db.init_app(app)

class Workers(db.Document):
  Names = db.StringField()
  Work = db.StringField()
  WorkerId = db.IntField()
  def to_json(self):
    return {"Names": self.Names,
        "Work": self.Work,
        "WorkerId" : self.WorkerId}

@app.route("/")
def root_path():
  return("Welcome")

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


@app.route('/user/', methods=['GET'])
def get_user():
  workers = Workers.objects()
  print(workers)
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    return  jsonify(workers)

def test_get():
    client  = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.get_data()

@app.route('/user/', methods=['POST'])
def add_user():
  record = json.loads(request.data)
  workers = Workers(Names=record['Names'],
        Work=record['Work'],
        WorkerId=record["WorkerId"])
  workers.save()
  return jsonify(workers)

def test_post():
    client = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.status_code==200

@app.route('/user/<id>', methods=['PUT'])
def Update_user(id):
  record = json.loads(request.data)
  workers = Workers.objects.get_or_404(id=id)
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    workers.update(Names=record['Names'],
          Work=record['Work'],
          WorkerId=record["WorkerId"])
  return jsonify(workers)


def test_put():
    client = app.test_client()
    url = '/user/634f246af10b5f16704aa3cf/'
    response = client.get(url)
    assert response.status_code==404
    

@app.route('/user/<id>/d', methods=['DELETE'])
def delete_user(id):
  workers = Workers.objects(id=id)
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    workers.delete()
  return jsonify(workers)

def test_del():
    client = app.test_client()
    url = '/user/634d2edb52df5a21b906aeb9/d'
    response = client.get(url)
    assert response.status_code==405



class Batch(db.Document):
  Names = db.StringField()
  Course = db.StringField()
  def to_json(self):
    return {"Names": self.Names,
        "Course": self.Course,}

@app.route('/batch/', methods=['GET'])
def get_batch():
  print('1')
  batch1 = Batch.objects()
  if not batch1:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify(batch1)

@app.route('/batch/', methods=['POST'])
def add_batch():
  record = json.loads(request.data)
  batch1 = Batch(Names=record['Names'],
        Course=record['Course'])
  batch1.save()
  return jsonify(batch1)



app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

if __name__ == "__main__":
  app.run(debug=True)

