# CampusLink Development Setup Guide

This document provides instructions for setting up the CampusLink development environment. CampusLink is a web application with a Django backend and Vue.js frontend.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- PostgreSQL 12 or higher
- Git

## Backend Setup (Django)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd CampusLink
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**

   Create a `.env` file in the project root with the following variables:

   ```
   SECRET_KEY=your_secret_key
   DB_NAME=campuslink_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. **Create the database**

   ```bash
   # Login to PostgreSQL
   psql -U postgres
   
   # Create the database
   CREATE DATABASE campuslink_db;
   
   # Exit PostgreSQL
   \q
   ```

7. **Run migrations**

   ```bash
   python manage.py migrate
   ```

8. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

9. **Start the Django development server**

   ```bash
   python manage.py runserver
   ```

   The backend will be available at http://localhost:8000/

## Frontend Setup (Vue.js)

1. **Navigate to the frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   # or if you use yarn
   yarn install
   ```

3. **Start the development server**

   ```bash
   npm run dev
   # or if you use yarn
   yarn dev
   ```

   The frontend will be available at http://localhost:5173/

## API Proxy Configuration

The frontend is configured to proxy API requests to the backend. This is set up in the Vite configuration and should work out of the box as long as the backend is running on http://localhost:8000/.

## Development Workflow

1. Run both the backend and frontend servers simultaneously
2. Make changes to the code
3. For frontend changes, the development server will automatically reload
4. For backend changes, you may need to restart the Django server depending on the changes made

## Project Structure

- `apps/` - Django applications
  - `accounts/` - User authentication and profiles
  - `cds/` - Central Department Store functionality
  - `entrepreneurs_hub/` - Entrepreneur Hub functionality
  - `laundry/` - Laundry Service functionality
- `backend/` - Django project settings and configuration
- `frontend/` - Vue.js frontend application
  - `src/` - Source code
    - `views/` - Vue components for different pages
    - `components/` - Reusable Vue components
    - `router/` - Vue Router configuration
    - `assets/` - Static assets

## Dependencies

### Backend Dependencies

- Django >= 4.0
- Django REST Framework
- django-cors-headers
- djangorestframework-simplejwt
- psycopg2-binary

### Frontend Dependencies

- Vue 3
- Vue Router
- Axios
- Pinia
- Vite
- ESLint
- Prettier
- Tailwind CSS

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues, ensure:

1. PostgreSQL is running
2. The database credentials in your `.env` file are correct
3. The database exists

### Frontend API Connection Issues

If the frontend cannot connect to the backend API:

1. Ensure the backend server is running
2. Check that CORS settings in `backend/settings.py` include your frontend URL
3. Verify the API endpoint URLs in your frontend code

### Node.js Version Issues

If you encounter issues with Node.js dependencies, ensure you're using a compatible version of Node.js. This project works best with Node.js 16 or higher.