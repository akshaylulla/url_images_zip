from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import json
import tempfile
import os
import shutil
import urllib.request

app = Flask(__name__)
socketio = SocketIO(app)

thread = None
thread_lock = Lock()

@app.route("/")
def hello_world():
  return render_template('index.html')

def background_thread():
  file_reader = open('main_test.json')
  json_data = json.load(file_reader)
  picture_dir = tempfile.mkdtemp()
  retrieve_all_files(picture_dir, json_data)
  file_reader.close()
  create_zip(picture_dir)
  send_zip()
  global thread
  thread = None

@socketio.event
def connect():
  global thread
  with thread_lock:
      if thread is None:
          thread = socketio.start_background_task(background_thread)
  emit('my_response', {'count': 0})

# retrieves jpeg, gif etc from a url and stores it in a file
def create_file(url, filename, picture_dir):
  picture_path = os.path.join(picture_dir, filename)
  local_filename, headers = urllib.request.urlretrieve(url, picture_path)

# Calls create_file, on each iteration through json, to download & save each file in a folder
def retrieve_all_files(picture_dir, json_data):
  counter = 0
  json_length = len(json_data)
  socketio.sleep(1)
  socketio.emit('my_length', {'json_length': json_length})
  socketio.emit('processing_start', {'complete': 'Processing Data'})
  for i in json_data:
      create_file(i['url'], i['filename'], picture_dir)
      socketio.sleep(0.2)
      counter += 1
      socketio.emit('my_response', {'count': counter})

# Creates the return_dir.zip, which is later sent to the client 
def create_zip(picture_dir):
  if os.path.exists(os.path.join(os.getcwd(), 'return_dir.zip')):
      os.remove(os.path.join(os.getcwd(), 'return_dir.zip'))
  socketio.emit('processing_end', {'complete': 'Creating Zip File'})
  socketio.sleep(0.5)
  shutil.make_archive('return_dir', 'zip', picture_dir)
  shutil.rmtree(picture_dir)

# Sends the return_dir.zip to the client
def send_zip():
  with open('return_dir.zip', 'rb') as f:
      zip_data = f.read()
  socketio.emit('zip_start', {'complete': 'Sending Zip Data'})
  socketio.sleep(0.5)
  socketio.emit('my_zip', {'zip_data': zip_data})
  socketio.sleep(0.5)
  socketio.emit('zip_completion', {'complete': 'Zip Data sent'})

if __name__ == "__main__":
  socketio.run(app)