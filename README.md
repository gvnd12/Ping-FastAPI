# Ping - FastAPI

A production-oriented social media backend built with **FastAPI**, designed around a modular architecture and modern backend practices. The project demonstrates scalable API design, JWT authentication, graph databases, object storage, and asynchronous programming.

## Features

- JWT-based Authentication & Authorization
- User Registration & Login
- User Profile Management
- Post Creation with Image Upload
- Like & Comment System
- Follow Relationships using Neo4j
- Admin APIs for User Management
- Object Storage using MinIO
- Redis Integration
- Modular FastAPI Architecture
- Async API Endpoints
- Request Validation using Pydantic


## Tech Stack

### Backend

- FastAPI
- Python 3.12

### Databases

- MongoDB
- Neo4j

### Storage

- MinIO

### Authentication

- JWT
- Passlib (bcrypt)


## Project Structure

```
backend/
│
├── app/
│   ├── api/
│   │   ├── auth/
│   │   ├── user/
│   │   └── admin/
│   │
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── query/
│   ├── schemas/
│   ├── tools/
│   └── utils/
│
├── main.py
├── pyproject.toml
└── README.md
```


## Core Functionality

### Authentication

- User Registration
- Secure Login
- JWT Access Tokens
- Password Hashing with bcrypt

### User

- Create Account
- Edit Profile
- Change Password
- View Profile

### Posts

- Create Posts
- Upload Images
- Like Posts
- Comment on Posts

### Social Graph (Not yet implemented)

Neo4j is used to efficiently model relationships such as:

- Follow
- Followers
- Social connections

This allows graph traversal to be significantly more efficient than traditional relational approaches for social networking features.


## Highlights

- Modular project structure
- Async request handling
- Clean separation of API, business logic, and database layers
- Object storage support for media uploads
- Production-style configuration management


## Running Locally

```bash
git clone https://github.com/gvnd12/Ping-FastAPI.git

cd Ping-FastAPI/backend

uv sync

uv run main.py
```

Configure the required environment variables before starting the application.


## Future Improvements

- Graph database integration for social relationships
- API Rate Limiting
- Notifications
- Real-time Chat using WebSockets
- Feed Recommendation Engine
- Search & Hashtags


## Disclaimer

This repository showcases the backend implementation developed as a personal learning project. It focuses on backend architecture and API design.

## Author

**Govind S S**

- GitHub: https://github.com/gvnd12
- LinkedIn: https://www.linkedin.com/in/govind-s-s
- Email: govindshaju@gmail.com
