# Contacts-API
A contacts api built using django rest framework

# Features 
- Authentication: I implemented token-based authentication to fortify the API against unauthorized access. Utilizing DRF's authentication classes, i ensure secure communication between clients and the API
- CRUD Operations: Leveraging the power of Django Rest Framework to seamlessly perform Create, Read, Update, and Delete operations on contacts.

# Installation Guide

- Download or clone this repostory using
  ```sh
  git clone git@github.com:SteppaCodes/Contacts-API.git
- Navigate into your project directory
  ```sh
  cd contacts-api
- Create a virtual environment
  ```sh
  python -m venv env
- Activate the virtual environment
- On Windows:
  ```sh
  env\scripts\activate
- On Macos:
  ```sh 
  source env/bin/activate
- Install dependencies
  ```sh
  pip install -r requirements.txt
- Run migrations to setup initial database schema
  ```sh
  python manage.py migrate
- Create super user(optional)
  ```sh
  python manage.py createsuperuser
- Run the development server
  ```sh
  python manage.py runserver
- Access the API: on your browser, navigate to
   ``` sh
    http://127.0.0.1:8000/api/v1/

# API Endpoints
- /api/v1/contacts/

  GET: Retrieve a list of all contacts or create a new contact.
  
  POST: Create a new contact.
  
- /api/contacts/{id}/

  GET: Retrieve details of a specific contact.
  
  PUT: Update details of a specific contact.
  
  DELETE: Delete a specific contact.

# Authentication
Token-based authentication is used to secure the API endpoints. To access protected endpoints, include the token in the request headers:

# Permissions
Permissions are implemented to control access to the API endpoints. By default, only authenticated users can access the endpoints. You can customize permissions according to your requirements.

Congratulations! You've successfully set up the Contacts API. If you encounter any issues or have any questions, feel free to reach out to me. Happy coding! 🚀
