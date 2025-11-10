🧠 AI Tutor – Django + Groq LLM Powered Learning App

AI Tutor is a Django-based web application that allows users to register, log in, and interact with an AI-powered tutoring assistant.
It uses Groq Llama-3.3 70B for fast and accurate AI responses.
The platform also includes user authentication, a dashboard, and quiz generation.

✅ Features
🔐 Authentication

User registration

User login

Secure logout

Multi-user support

🎓 AI Tutor

Chat with Groq Llama model

Explains concepts

Solves problems

Generates quizzes

📝 Quiz Generator

Create AI-generated questions

Evaluate answers

🖥️ Dashboard

Personalized user dashboard

Access chat, quizzes, and learning tools

🛠️ Tech Stack
Layer	Technology
Backend	Django 5, Django REST Framework
AI Model	Groq Llama-3.3 70B
Frontend	HTML, CSS (Inline), Bootstrap (optional)
Database	SQLite (local), PostgreSQL (production optional)
Deployment	PythonAnywhere / Render / Railway
📦 Installation (Local)
1️⃣ Clone the repository
git clone https://github.com/Rishavkumar720/ai_tutor.git
cd ai_tutor

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set environment variables
setx GROQ_API_KEY "your-api-key"
setx DJANGO_SECRET_KEY "your-django-secret"

5️⃣ Run migrations
python manage.py migrate

6️⃣ Start server
python manage.py runserver

🚀 Deployment (PythonAnywhere)

Zip the project folder

Upload to PythonAnywhere

Create a virtualenv

Install requirements

Configure WSGI + static files

Add environment variables

Reload the web app

📁 Project Structure
ai_tutor/
│── backend/
│   ├── backend/        # Project settings
│   ├── tutor/          # App with AI logic
│   ├── templates/      # HTML files
│   ├── static/         # CSS/JS/images
│── requirements.txt
│── Procfile (if deployed on Render)

🔑 Environment Variables
Variable	Description
GROQ_API_KEY	API key for Groq
DJANGO_SECRET_KEY	Django security key
DATABASE_URL	(Optional) for PostgreSQL on cloud
🙌 Contributing

Pull requests are welcome.
For major changes, open an issue first.

📜 License

This project is under the MIT License.
