# RADify

> Transform any work order into a professional Requirement Analysis Document (RAD) effortlessly.

---

## 📜 Project Overview

**RADify** is an AI-powered web application that generates high-quality Requirement Analysis Documents (RAD) from uploaded Work Orders or Work Specifications (PDF/Word format).  
The generated RAD is automatically saved to a specified folder in the user's Google Drive.

Built with a modern tech stack:

- **CrewAI** (for intelligent RAD generation)
- **FastAPI** (for robust backend APIs)
- **Angular 17 + TypeScript** (for a sleek and dynamic frontend)
- **MySQL** (for secure user data storage)
- **Google Drive Integration** (to save documents directly to the user's Drive)

---

## ✨ Key Features

- 🔐 **User Management** (Sign Up, Sign In, Forgot Password, Gmail OAuth Login)
- ☁️ **Google Drive Integration** (OAuth 2.0 Authorization)
- 📄 **Upload Work Specifications** (PDF, Word Documents)
- 🧠 **AI Agent-powered RAD Generation** (CrewAI)
- 📂 **Save RAD Documents** (directly into a designated Google Drive folder)
- 📊 **Clean Dashboard and Simple Workflow**

---

## 🛠️ Tech Stack

| Layer | Technology |
|:-----|:------------|
| Frontend | Angular 17, TypeScript |
| Backend | FastAPI (Python) |
| AI Agent | CrewAI Framework |
| Database | MySQL |
| Authentication | JWT, Google OAuth 2.0 |
| Cloud Storage | Google Drive API |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL Database
- Google Cloud Project (for OAuth2 credentials)
- Git

### Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup(Angular)
```bash
cd frontend
npm install
ng serve --open
```

### Folder Structure
```bash
radify/
├── backend/
│   ├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── src/
│   ├── angular.json
│   └── ...
├── README.md
└── LICENSE
```

### Security

- Passwords are encrypted.
- JWT-based authentication is used.
- OAuth tokens are stored securely.
- Google Drive access is limited to the app's created folders.

### License
This project is licensed under the GNU Public Licence.

### Contact
You can email Argha Dey Sarkar[email2argha@gmail.com] for any assistance.
