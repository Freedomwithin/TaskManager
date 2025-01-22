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
git clone [your-github-repo-url]
cd taskmanager-electron

### Python Environment Setup
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

### Node Dependencies
npm install

## 🚀 Running the Application

### Development Mode
Flask Server

python run.py

Electron App
npm start

### Production Deployment
gunicorn --workers 3 --bind 0.0.0.0:5001 wsgi:app
