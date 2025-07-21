## Usage
### Setup
Clone this repository and stay in the parent -```task```- directory. 
Set up a virtual environment, here is a quick guide for unix systems:
```
python -m venv venv
source venv/activate/bin
pip install -r requirements.txt
```
### Running the Server
Navigate to project directory, ```task/filesync```. Run:
```
python manage.py migrate
python manage.py makemigrations files
python manage.py migrate
python manage.py runserver
```
### Viewing the Admin Page
Once the server is up and running, you can check out the admin page at ```localhost:8000/admin```.  This can be used as an additional method to verify that files are being stored in the django database in the destination directory.

Admin details are available upon request.

### Running the Application
Navigate to the parent directory of the project, ```task```. Run:
```
python sync_app.py
```
This will let you know that it is listening to the source dir-```task/data/files```. When you change anything file related in the source dir, it will output the status accordingly. 
If not already created, the destination directory will be made in ```task/filesync/data/files```
The server must be running for this application to work

### Testing the project
To run tests on the Django backend:
```
cd task/filesync
python manage.py test files
```
To run tests on the CLI applcation:
```
cd task
pytest test_sync_app.py
```
