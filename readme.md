Program Overview - 
- Technologies used - flask (Python), jquery, socketIO  
- Open sample.json file containing urls and file names.
- Iterate through urls, download contents from url, and save to file and add to temp folder
- Create zip from temp folder and delete temp folder
- Send zip data (bytes) to client
- Client converts bytes to zip file and zip file is downloaded

Instructions to Run - 
- Download repository from Github
- Navigate to repository in a terminal window
- Install dependencies using 'pip3 install -r requirements.txt' or activate venv (if virtualenv is installed) using 'source bin/activate'
- Use command "python3 site.py" to start the server
- Navigate to url 'http://127.0.0.1:5000/' in a browser window
- The program begins to retrieve the files based on the 'main_test.json' file (100 urls/jpegs). It also sends a status counter to the client and eventually, a zip file is downloaded by the client. 

Note - To run/test the program quicker, you could switch 'main_test.json' in 'site.py' with 'small.json' (small.json contains the 12 urls to the gifs).