# CampusLink Development Environment Setup

This guide will help you set up the CampusLink project on a new device.

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **PostgreSQL 12+** - [Download here](https://www.postgresql.org/download/)
- **Git** - [Download here](https://git-scm.com/downloads/)
- **Redis** (optional, for caching and background tasks) - [Download here](https://redis.io/download)

### Verify installations:

```bash
python --version    # Should show Python 3.8+
node --version      # Should show Node.js 16+
npm --version       # Should come with Node.js
psql --version      # Should show PostgreSQL 12+
git --version       # Should show Git version
```

## Project Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd CampusLink
```

### 2. Backend Setup (Django)

#### Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Database Setup

1. **Create PostgreSQL Database:**

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database and user
CREATE DATABASE campuslink_db;
CREATE USER campuslink_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE campuslink_db TO campuslink_user;
\q
```

2. **Create Environment Variables File:**
   Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_NAME=campuslink_db
DB_USER=campuslink_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=True
```

#### Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser

```bash
python manage.py createsuperuser
```

#### Load Sample Data (optional)

```bash
# sql script to load data
```

### 3. Frontend Setup (Vue.js)

#### Navigate to Frontend Directory

```bash
cd frontend
```

#### Install Node Dependencies

```bash
npm install
```

#### Create Frontend Environment File

Create `.env` file in the `frontend` directory:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Running the Application

### Method 1: Run Both Servers Separately

#### Terminal 1 - Backend Server

```bash
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Run Django development server
python manage.py runserver
```

Backend will be available at: http://127.0.0.1:8000

#### Terminal 2 - Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

### Method 2: Using Package Scripts

Create these scripts in your root `package.json`:

```json
{
  "name": "campuslink",
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd .. && python manage.py runserver",
    "dev:frontend": "cd frontend && npm run dev",
    "install:all": "pip install -r requirements.txt && cd frontend && npm install"
  },
  "devDependencies": {
    "concurrently": "^8.2.2"
  }
}
```

Then run:

```bash
npm install concurrently
npm run dev
```

## Database Management

### Common Django Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py shell
python manage.py test
```

## Recommended VS Code Extensions

For the best developer experience, install these extensions in VS Code:

### Vue.js Development

- [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)  
  _(Essential for Vue 3 syntax highlighting, IntelliSense, and type checking)_

### Django/Python Development

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)  
  _(Syntax highlighting, linting, and debugging for Python)_
- [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django)  
  _(Template syntax, code snippets, and navigation for Django)_

### Code Formatting & Linting

- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)  
  _(Automatic code formatting for JS, Vue, CSS, etc.)_
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)  
  _(JavaScript/Vue linting and error highlighting)_

---

**After installing these extensions, enable "Format On Save" in your VS Code settings for automatic formatting.**

## Common Issues & Solutions

### Issue 1: PostgreSQL Connection Error

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**

- Make sure PostgreSQL service is running
- Check database credentials in `.env` file
- Verify database exists: `psql -U postgres -l`

### Issue 2: Node Modules Error

**Error:** `Module not found` or `Cannot resolve dependency`

**Solution:**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue 3: Python Virtual Environment Issues

**Error:** `Command not found` or module import errors

**Solution:**

- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Issue 4: CORS Errors

**Error:** `CORS policy: Cross origin requests are blocked`

**Solution:**

- Check `CORS_ALLOWED_ORIGINS` in `backend/settings.py`
- Make sure frontend URL is included

## Production Deployment Notes

When deploying to production:

1. **Environment Variables:**

   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure proper database credentials

2. **Static Files:**

   - Configure proper static file serving
   - Use CDN for media files

3. **Security:**
   - Configure `ALLOWED_HOSTS`
   - Set up HTTPS
   - Configure CORS properly

---

# Daily Development Workflow

**Follow these steps every time you pull new changes or start work. This ensures everyone’s backend, database, and environment are consistent.**

---

##  Sync Your Codebase

- Pull the latest code (and migration files) from your main branch:
    ```bash
    git checkout main   # or your project’s main branch
    git pull
    ```

---

##  Update Virtual Environment and Python Dependencies (Stay on project root)

- If your virtual environment is not active, activate it:
    ```bash
    # On Windows
    venv\Scripts\activate
    # On Mac/Linux
    source venv/bin/activate
    ```
- Install any new requirements:
    ```bash
    pip install -r requirements.txt
    ```

---


##  Run Django Migrations

- **Always run migrations after pulling code:**
    ```bash
    python manage.py migrate
    ```

---

##  Update Frontend

    ```bash
    cd frontend
    npm install
    ```

---


##  Start Your Servers

- Backend:
    ```bash
    python manage.py runserver
    ```
- Frontend :
    ```bash
    npm run dev
    ```

---

## 👥 Team Collaboration Best Practices

- **Never** manually delete or edit migration files unless everyone on the team resets together.
- If you see migration errors, **communicate first**—don’t try to fix it solo.
- Only **one person at a time** should make big model or migration changes.
- In production, **never** drop the DB or delete migrations—always use migrations to change schema.

---

## 💡 TL;DR (Quick Reference)

```bash
git pull
pip install -r requirements.txt
python manage.py migrate
cd frontend && npm install


1. Activate virtual environment
2. Pull latest changes: `git pull`
3. Install any new dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
4. Run migrations: `python manage.py migrate`
5. Start development servers



## Useful Development Tools

### Django Admin

Access at: http://127.0.0.1:8000/admin

### API Documentation

- Django REST Framework browsable API: http://127.0.0.1:8000/api/

### Database GUI Tools

- pgAdmin (for PostgreSQL)
- DBeaver (cross-platform)

## Support

If you encounter issues:

1. Check this documentation first
2. Look at error logs in terminal
3. Search for error messages online
4. Check Django/Vue.js documentation
5. Create an issue in the project repository

---
