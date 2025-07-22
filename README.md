## Usage
### Setup
Clone this repository and set up a virtual environment, here is a quick guide for unix systems:
```
python -m venv venv
source venv/activate/bin
pip install -r filesync/requirements.txt
```
### Running the Server
Navigate to project directory, ```filesync_task/filesync```. Run:
```
python manage.py migrate
python manage.py makemigrations files
python manage.py migrate
python manage.py runserver
```
The migrations may not be necessary once the server has been ran once, but it prevents any headaches.

### Viewing the Admin Page
Once the server is up and running, you can check out the admin page at ```localhost:8000/admin```.  This can be used as an additional method to verify that files are being stored in the django database in the destination directory.

Admin details are available upon request.

### Running the Application
Navigate to the project directory, Run:
```
python sync_app.py
```
This will let you know that it is listening to the source dir-```filesync_task/data/files```. When you change anything file related in the source dir, it will output the status accordingly. 
If not already created, the destination directory will be made in ```filesync_task/filesync/data/files```
The server must be running for this application to work

### Testing the project
To run tests on the Django backend:
```
cd filesync_task/filesync
python manage.py test files
```
To run tests on the CLI applcation:
```
cd filesync_task/filesync
pytest
```

## Improvements

Due to personal time contraints, I did not implement the following however they were considered:

- Chunking
- User account creation and authentication (tokenisation perhaps)
- File versions and rollback functionality
