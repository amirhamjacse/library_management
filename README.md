# Library Management API

## Overview
The Library Management API is a backend system that facilitates book management, borrowing, and returning functionalities for a library. It provides secure authentication using JWT and implements role-based access control for users (members) and administrators.

## Features
- **JWT Authentication**: Secure login and token-based authentication.
- **Role-Based Access Control**:
  - Admin: Can manage books (CRUD operations).
  - Member: Can view books, borrow, and return books.
- **Book Borrowing System**:
  - Members can borrow up to 5 books.
  - Books have a return deadline (e.g., 14 days from borrowing date).
  - Late returns incur fines (e.g., 5 BDT per day).
- **Concurrency Handling**: Prevents multiple users from borrowing the same book simultaneously.

## Technology Stack
- Django
- Django Rest Framework (DRF)
- Simple JWT (for authentication)
- PostgreSQL or SQLite (Database)

## Installation & Setup
### Prerequisites
- Python 3.9 installed
- Virtual environment

### Installation Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/amirhamjacse/library_management
   cd library_management
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Copy the example environment file and configure the database settings:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and update the database configuration:
     ```ini
     DB_NAME=your_database_name
     DB_USER=your_database_user
     DB_PASSWORD=your_database_password
     DB_HOST=your_database_host
     DB_PORT=your_database_port
     ```
5. **Run migrations**
   ```bash
   python manage.py migrate
   ```
6. **Create a superuser (Admin account)**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints
### Authentication
- **Login (Obtain JWT Token):**
  ```http
  POST /api/token/
  ```
  **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```
  **Response:**
  ```json
  {
    "access": "<JWT_ACCESS_TOKEN>",
    "refresh": "<JWT_REFRESH_TOKEN>"
  }
  ```

### Books Management (Admin Only)
- **Create a new book**
  ```http
  POST /book/list-create/
  ```
- **Retrieve all books**
  ```http
  GET /book/list-create/
  ```
- **Retrieve a book's details**
  ```http
  GET /book/details/{book_id}/
  ```
- **Update a book**
  ```http
  PUT /book/details/{book_id}/
  ```
- **Delete a book**
  ```http
  DELETE /book/details/{book_id}/
  ```

### Borrowing & Returning Books (Members Only)
- **Borrow a book**
  ```http
  POST /book/borrow/{book_id}/
  ```
- **Return a book**
  ```http
  POST /book/return/{book_id}/
  ```
- **Retrieve borrowed books**
  ```http
  GET /book/borrowed/
  ```

## Role-Based Access Control
- **Admin Role:** Full control over books.
- **Member Role:** Can only view, borrow, and return books.
- **Permissions are enforced using Django permissions and DRF view-level permissions.**

## Handling Fines
- Late returns incur fines at a rate of **5 BDT per day**.
- Fine calculation is automated upon return.


## Author
[Amir Hamja](https://github.com/your-github-profile)

