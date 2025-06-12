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

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Configuration (if using)
REDIS_URL=redis://localhost:6379/0

# bKash API Configuration (when ready)
BKASH_APP_KEY=your_bkash_app_key
BKASH_APP_SECRET=your_bkash_app_secret
BKASH_USERNAME=your_bkash_username
BKASH_PASSWORD=your_bkash_password
BKASH_BASE_URL=https://tokenized.sandbox.bka.sh/v1.2.0-beta
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
# If you have fixtures
python manage.py loaddata sample_data.json
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
VITE_BKASH_SCRIPT_URL=https://scripts.sandbox.bka.sh/versions/1.2.0-beta/checkout/bKash-checkout-sandbox.js
```

## Running the Application

### Method 1: Run Both Servers Separately

#### Terminal 1 - Backend Server
```bash
# On Windows:
campuslink_env\Scripts\activate

# On macOS/Linux:
source campuslink_env/bin/activate

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

### Method 2: Using Package Scripts (Recommended)
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

### Database Reset (if needed)
```bash
python manage.py flush
python manage.py migrate <app_name> zero
python manage.py migrate <app_name>
```

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

### Issue 5: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

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

## Development Workflow

### Daily Development
1. Activate virtual environment
2. Pull latest changes: `git pull`
3. Install any new dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
4. Run migrations: `python manage.py migrate`
5. Start development servers

### Before Committing
1. Run tests: `python manage.py test`
2. Check code formatting: `flake8` (if configured)
3. Update requirements if new packages added:
   ```bash
   pip freeze > requirements.txt
   ```

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
