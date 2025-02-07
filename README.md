# Job Log Management System

A Django-based application to manage job logs for various units. The application allows terminal heads and unit heads to view and download reports for their respective units.

## Features


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Django 3.2 or higher
- pip (Python package installer)

## Getting Started

Follow these instructions to set up the project locally.

### 1. Clone the repository

```sh
git clone https://github.com/your-username/job-log-management.git
cd job-log-management
```

### 2. Set up a virtual environment

It's recommended to use a virtual environment to manage dependencies.

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

Install the required Python packages using pip.

```sh
pip install -r requirements.txt
```

### 4. Set up the database

Run the following commands to create the necessary database tables and apply migrations:

```sh
python manage.py migrate
```

### 5. Create a superuser

Create an admin user to access the Django admin panel. In your terminal, open your python shell. 

To open your python shell:

 python manage.py shell

To create the super admin, please follow this command:

```sh

from admin_area.models import SuperAdmin
from django.contrib.auth.hashers import make_password


super_admin = SuperAdmin()
super_admin.first_name = "Super"
super_admin.last_name = "Admin"
super_admin.email = "your_email@example.com"
password = "your_password"
super_admin.password = make_password(password)
super_admin.save()
```

### 6. Run the development server

Start the Django development server.

```sh
python manage.py runserver
```

### 7. Access the application

Open your web browser and navigate to `http://127.0.0.1:8000`.

## Project Structure



## Environment Variables

The project requires the following environment variables to be set. Create a `.env` file in the project root and add the variables:

```env
SECRET_KEY='your-secret-key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .localhost
```

## Running Tests

To run the tests, execute:

```sh
python manage.py test
```

## Deployment

For deployment, ensure the following:

1. Set `DEBUG=False` in `settings.py`.
2. Use a production-ready database (e.g., PostgreSQL).
3. Set up a web server (e.g., Gunicorn) and reverse proxy (e.g., Nginx).

## Contributing

To contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/feature-name`).
3. Make your changes and commit them (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature/feature-name`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Openpyxl](https://openpyxl.readthedocs.io/)

```

This README file provides clear instructions on how to download, set up, and run the Django project locally, as well as how to contribute to it. Be sure to replace `https://github.com/your-username/job-log-management.git` with the actual URL of your GitHub repository.
