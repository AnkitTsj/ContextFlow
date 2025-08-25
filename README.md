# ContextBridge – Production README

ContextBridge is a chat context and extraction platform with secure user accounts and per-user session history.

## Features

- FastAPI backend (Python 3.11+)
- Secure JWT authentication (per-user context isolation)
- User registration (hashed passwords)
- Chat/context upload and extraction
- Session export, copy, retrieve, and delete (per user)
- Modern React frontend

---

## Installation

1. **Clone the repository**

2. **Install Python dependencies:**

pip install -r requirements.txt


3. **Set your SECRET_KEY env variable (very important!):**
- On Linux/Mac:
  ```
  export SECRET_KEY='your-very-long-random-prod-secret'
  ```
- On Windows:
  ```
  set SECRET_KEY=your-very-long-random-prod-secret
  ```

4. **Run the Backend:**

uvicorn app.main:app --reload


5. **(Recommended) Docker Build:**
 ```
 docker build -t contextbridge-backend .
 docker run -p 8000:8000 -e SECRET_KEY=your-very-long-random-prod-secret contextbridge-backend
 ```

---

## Production Deployment

- Build and run the backend with Docker (see above) or a trusted Python host.
- Use a reverse proxy (nginx, caddy) or deployment platform to put your API/React app behind HTTPS.
- Store per-user sessions and users.json in persistent storage.
- [Optional] Use managed secrets to store your environment variables in the cloud.

---

## Contribution

Open PRs or issues for bugs and improvements.
