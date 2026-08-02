# Ping Frontend

Minimal React (JavaScript) frontend for the Ping FastAPI backend, built with Vite, React Router, axios, and [motion.dev](https://motion.dev) for animations.

## Scope

This UI intentionally covers only the endpoints the backend currently exposes:

- Auth: login, logout
- Account: signup, edit profile, change password, deactivate, delete
- Posts: create post (image + caption), like a post by id, comment on a post by id
- Admin: list users, undelete a user

### Known limitations (driven by the backend)

- There is no `/me` or profile read endpoint, so Account Settings forms are write-only and cannot pre-fill your current values.
- There is no feed / list-posts endpoint, so Like and Comment require manually entering a `post_id`.
- There is no image-serving endpoint, so uploaded post images are not displayed anywhere.

## Setup

```bash
npm install
npm run dev
```

The app runs on `http://localhost:5173`.

Configure the backend URL via `.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

## Backend

Run the FastAPI backend on `http://localhost:8000`. CORS for `http://localhost:5173`
is enabled in `backend/main.py`.

Admin access is derived by decoding the JWT `context.user_type` claim client-side;
logging in with the super-admin credentials routes you to the admin users table.
