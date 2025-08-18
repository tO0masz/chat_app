Chat App 💬



Real-time chat application built with Django and WebSockets using Channels.
The project uses PostgreSQL as the database (via Docker) and Redis as the channel layer (via Docker).



🚀 Features


Real-time chat with WebSockets

Django Channels with Redis as the channel layer

PostgreSQL as the database

HTMX for dynamic frontend interactions

Fully containerized environment with Docker Compose



🛠 Tech Stack


Backend: Django 4.2+, Django Channels

WebSockets Server: Daphne

Database: PostgreSQL (Docker)

Channel Layer: Redis (Docker)

Frontend Enhancements: HTMX

Environment: Docker & Docker Compose



📂 Project Structure


CHAT_APP/

│── .vscode/               # VSCode settings (optional)

│── backend/               # Backend Django application

│   ├── chat_app/          # Main Django project

│   └── venv/              # Virtual environment (ignored in Git)

│── docker-compose.yml     # Docker Compose configuration (Postgres + Redis)

│── .gitignore             # Ignored files (venv, DB data, etc.)



⚙️ Requirements


Python 3.10+

Docker & Docker Compose

Virtual environment 

Python dependencies are listed in requirements.txt:

Django>=4.2.0,<5.0.0
python-dotenv>=1.0.0
channels>=4.0.0
channels-redis>=4.1.0
django-htmx>=1.17.0
redis>=4.6.0
asgiref>=3.7.0
daphne>=4.0.0



▶️ Getting Started


1. Clone the repository
git clone https://github.com/your-username/chat_app.git
cd chat_app

2. Create .env file

Create a .env file in the project root (next to docker-compose.yml) with content like:

POSTGRES_DB=chatdb
POSTGRES_USER=chatuser
POSTGRES_PASSWORD=chatpassword
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379



⚠️ Do not commit your .env file. Instead, provide an .env.example for contributors.


3. Start services with Docker
docker-compose up -d


This will spin up:

PostgreSQL database

Redis server

4. Run Django server

If you want to run Django locally (outside Docker):

cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver



🧪 Development Notes


Run migrations before first use:

python manage.py migrate


Create superuser:

python manage.py createsuperuser
