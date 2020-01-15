### Testing Python code in Shell

#### Create a virtual environment & activate it
python3 –m venv .venv
source .venv/bin/activate 

#### Output your pip library dependencies into a txt file for human reference
pip freeze > requirements.txt

#### Run the Flask server/app
python app.py

#### Call the app in a new browser window
http://0.0.0.0:8080/

#### It will auto-populate the full URL - remove the auth and replace with the function name
https://8080-dot-9252955-dot-devshell.appspot.com/?authuser=1&environment_name=default&environment_id=default
https://8080-dot-9252955-dot-devshell.appspot.com/food


#### Edit files in GCP using the File Explorer - see top right of Shell window


