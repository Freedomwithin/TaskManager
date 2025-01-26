# 📋 Task Manager Application

## 🚀 Project Overview
A robust task management application built with Flask (backend) and Electron (desktop frontend), enabling users to efficiently organize and track tasks.

## ✨ Key Features
- Task creation and management
- Persistent task storage
- Electron desktop interface
- Flask-powered backend
- Database-driven task tracking

## 🛠 Tech Stack
- **Backend:** Flask
- **Frontend:** Electron
- **Database:** SQLAlchemy
- **Language:** Python, JavaScript

## 🔧 System Requirements
- Python 3.8+
- Node.js
- pip
- npm

## 📦 Setup Instructions

### Clone Repository
   ```bash
git clone https://github.com/Freedomwithin/TaskManager
   ```
### Python Environment Setup

   ```bash
cd Taskmanager-main
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
   ```
### Node Dependencies
   ```bash
npm install
   ```
## 🚀 Running the Application

### Development Mode

Flask Server
   ```bash
python run.py
   ```
### Production Deployment
   ```bash
gunicorn --workers 3 --bind 0.0.0.0:5001 wsgi:app
   ```
## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE.md file for details.
