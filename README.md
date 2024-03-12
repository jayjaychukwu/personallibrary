# personallibrary

A Personal Library Management System API developed using Python, Django, Django REST Framework, PostgreSQL and Docker.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository into a folder of your choice:

   ```shell
   git clone https://github.com/jayjaychukwu/personallibrary.git
   ```

2. Enter the personallibrary directory and spin up the project using Docker Compose:

   Either you use

    ```shell
    docker-compose up --build
    ```

   and spin up another terminal to run the next set of commands or you run it in the background using

   ```shell
   docker-compose up -d --build
   ```

3. Make migrations for the accounts and chat app and migrate

   ```shell
   docker-compose exec web python manage.py makemigrations accounts books
   docker-compose exec web python manage.py migrate
   ```

4. Restart the web service

   ```shell
   docker-compose restart web  
   ```

- To create a superuser for the admin dashboard, run the following command:
  
    ```shell
    docker-compose exec web python manage.py createsuperuser
    ```

    Follow the prompts to create a superuser account.
    Access the admin dashboard at `http://localhost:8000/admin/` and log in using your superuser credentials.

## API Documentation

- Swagger Docs: `http://localhost:8000/`
- ReDoc: `http://localhost:8000/redoc/`

## Architecture

The project follows a Django architecture and utilizes the Django REST Framework for building the API. Docker is used for containerization, providing an isolated and consistent environment for development and deployment.

## Support and Feedback

- Remember to always spin down your docker containers after you are done because they can consume a lot of memory.

Please feel free to reach out to me or raise an Issue if you run into any problems running this project.
