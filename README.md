# Chat App 💬



Real-time chat application built with Django and WebSockets using Channels.
The project uses PostgreSQL as the database (via Docker) and Redis as the channel layer (via Docker).



## 🚀 Features


- Real-time chat with WebSockets

- Django Channels with Redis as the channel layer

- PostgreSQL as the database

- HTMX for dynamic frontend interactions

- Containerized environment with Docker Compose



## 🛠 Tech Stack


- **Backend:** Django 4.2+, Django Channels

- **WebSockets Server**: Daphne

- **Database:** PostgreSQL (Docker)

- **Channel Layer:** Redis (Docker)

- **Frontend Enhancements:** HTMX

- **Environment:** Docker & Docker Compose



## 📂 Project Structure


CHAT_APP/

│── .vscode/               # VSCode settings (optional)

│── backend/               # Backend Django application

│   ├── chat_app/          # Main Django project

│   └── venv/              # Virtual environment (ignored in Git)

│── docker-compose.yml     # Docker Compose configuration (Postgres + Redis)

│── .gitignore             # Ignored files (venv, DB data, etc.)



## ⚙️ Requirements


- **Python 3.10+**

- **Docker & Docker Compose**

- **Virtual environment** 

Python dependencies are listed in requirements.txt:

- **Django>=4.2.0,<5.0.0**

- **python-dotenv>=1.0.0**

- **channels>=4.0.0**

- **channels-redis>=4.1.0**

- **django-htmx>=1.17.0**

- **redis>=4.6.0**

- **asgiref>=3.7.0**

- **daphne>=4.0.0**

- **psycopg>=3.1.0**

- **psycopg2>=2.9.0**



## ▶️ Getting Started


1. Clone the repository
- **git clone https://github.com/tO0masz/chat_app.git**

- **cd chat_app**



⚠️ Do not commit your .env file. Instead, provide an .env.example for contributors.


2. Start services with Docker:

- **docker-compose up -d**


This will spin up:

- **PostgreSQL** database

- **Redis** server

3. Run Django server

If you want to run Django locally (outside Docker):

- **cd backend**

- **python -m venv venv**

- **source venv/bin/activate**   # On Windows: **venv\Scripts\activate**

- **pip install -r requirements.txt**

- **python manage.py migrate**

- **python manage.py runserver**



## 🧪 Development Notes


Run migrations before first use:

**python manage.py migrate**


Create superuser:

**python manage.py createsuperuser**
