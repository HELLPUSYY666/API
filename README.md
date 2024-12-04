# Project Overview

This project is a Python-based web application built with Django that allows users to create, like, and comment on posts. Each user has their own profile, enabling a personalized experience. The project also features JWT authentication for secure user login and session management.

## Features

- **Post Creation**: Users can create posts and share content with the community.
- **User Interaction**: Users can like posts and leave comments to engage with other users.
- **User Profiles**: Each user has their own profile page to view their posts and activity.
- **JWT Authentication**: Secure user authentication with JWT for a seamless login experience.
- **Testing**: The application includes unit tests for critical functionality to ensure stability.
- **Caching**: Utilizes Redis for caching data and enhancing performance.
- **CI/CD**: Integrated continuous integration and deployment pipelines for efficient development workflows.

## Tech Stack

- **Python 3.x**: The main programming language.
- **Django**: The primary web framework for building the server-side logic.
- **Django Rest Framework (DRF)**: Used for building RESTful APIs.
- **Redis**: Employed for caching and session management.
- **Unit Tests**: Written using Django's built-in test framework to ensure code quality.
- **CI/CD Pipelines**: Used for automated testing and deployment.

## Installation and Setup

### Requirements

Ensure you have Docker and Docker Compose installed on your system.

### Clone the Repository

```bash
git clone https://github.com/username/your-project-name.git
cd your-project-name
```

### Build and Run the Application
- Build the containers:

```docker-compose build```

- Start the application:

```docker-compose up```

This command will start the development server and make the application available at http://localhost:8000.

### Run Migrations
- To set up the database, run:
```docker-compose run web python manage.py migrate```

### Create a Superuser
- Create a superuser for accessing the Django admin:
```docker-compose run web python manage.py createsuperuser```

Follow the prompts to set up your superuser account.

### Run Unit Tests
- To ensure the application is functioning correctly, run the unit tests with:

```docker-compose run web python manage.py test```

### Usage

- Visit http://localhost:8000 to access the web application.
- Register an account or log in to create posts, like posts, and leave comments.
- Navigate to user profiles to see posts and activities.

### License

- This project is licensed under the MIT License. See the LICENSE file for more details.

### Author

Developer: Zakariya

