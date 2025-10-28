# 🚨 Pre-Deployment Environment Check

## Backend .env Analysis

### ✅ **Good Configurations:**
1. ✅ **Database**: AWS RDS MySQL configured
   - Host: `expensesense-infrastructure-rdsinstance-wkxdaqyhtfrb.cv8usc4coj2c.ap-south-1.rds.amazonaws.com`
   - Database: `expensesense_db`
   - User: `admin`
   - Region: `ap-south-1` (Mumbai)

2. ✅ **DEBUG Mode**: Correctly set to `False` for production

3. ✅ **Google OAuth**: Client ID configured

---

## 🔴 **CRITICAL SECURITY ISSUES** (Must Fix Before Deploy!)

### 1. **SECRET_KEY - INSECURE** 🚨
```properties
SECRET_KEY=django-insecure-dev-key-change-in-production-12345678990
```

**Problem**: Using development key in production!

**Fix**: Generate a strong secret key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Replace with**: A 50+ character random string like:
```
SECRET_KEY=x9#k@2m$p8n!q5w^r7t&y3u*i1o@k4l%j6h^g8f&d9s#a2w$e4r
```

---

### 2. **JWT_SECRET - INSECURE** 🚨
```properties
JWT_SECRET=jwt-secret-key-for-development-only-12345678990
```

**Problem**: Using development key for JWT signing!

**Fix**: Generate a strong JWT secret:
```bash
openssl rand -base64 64
```

**Replace with**: A cryptographically secure random string

---

### 3. **ALLOWED_HOSTS - TOO PERMISSIVE** 🚨
```properties
ALLOWED_HOSTS=[*]
```

**Problem**: Allows requests from ANY domain! Vulnerable to Host header attacks.

**Fix**: Specify your actual domain(s):
```properties
# For AWS deployment
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-ec2-ip-address

# Or if using AWS Elastic Beanstalk/ECS
ALLOWED_HOSTS=.elasticbeanstalk.com,.amazonaws.com,your-domain.com
```

**Example**:
```properties
ALLOWED_HOSTS=expensesense.com,www.expensesense.com,13.127.45.123
```

---

### 4. **CORS_ALLOWED_ORIGINS - TOO PERMISSIVE** 🚨
```properties
CORS_ALLOWED_ORIGINS=[*]
```

**Problem**: Allows CORS requests from ANY origin! Security risk.

**Fix**: Specify your frontend domain(s):
```properties
# For production
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# If testing locally too
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:3000
```

**Example**:
```properties
CORS_ALLOWED_ORIGINS=https://expensesense.com,https://www.expensesense.com
```

---

### 5. **Database Password Exposed** ⚠️
```properties
DB_PASSWORD=SelvaSam123#
```

**Problem**: Password visible in plain text (acceptable in .env but ensure .env is in .gitignore)

**Recommendation**:
- ✅ Ensure `.env` is in `.gitignore`
- ✅ Use AWS Secrets Manager or SSM Parameter Store for production
- ✅ Rotate password after initial setup

---

## 📝 **Recommended Production .env**

Here's a secure configuration template:

```properties
# Database Configuration
DB_NAME=expensesense_db
DB_USER=admin
DB_PASSWORD=SelvaSam123#
DB_HOST=expensesense-infrastructure-rdsinstance-wkxdaqyhtfrb.cv8usc4coj2c.ap-south-1.rds.amazonaws.com
DB_PORT=3306

# Django Settings
SECRET_KEY=<GENERATE_NEW_50_CHAR_SECRET>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-ec2-ip

# JWT Configuration
JWT_SECRET=<GENERATE_NEW_JWT_SECRET>

# Google OAuth
GOOGLE_CLIENT_ID=927865345975-bp9rjjf7tucsq86q6affu9iq3sddpigu.apps.googleusercontent.com

# CORS Settings
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# Additional Production Settings (Add these)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

## 🔧 **Generate Secure Keys**

### Generate Django SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Generate JWT_SECRET:
```bash
openssl rand -base64 64 | tr -d '\n' && echo
```

Or in Python:
```bash
python -c 'import secrets; print(secrets.token_urlsafe(64))'
```

---

## 🌐 **Frontend .env Check**

### Current Configuration:
```properties
API_BASE_URL=http://localhost:8000
GOOGLE_CLIENT_ID=927865345975-bp9rjjf7tucsq86q6affu9iq3sddpigu.apps.googleusercontent.com
```

### ⚠️ **Issues:**

1. **API_BASE_URL** - Points to localhost!
   
   **Fix for production**:
   ```properties
   API_BASE_URL=https://api.your-domain.com
   # or
   API_BASE_URL=https://your-backend-url.elasticbeanstalk.com
   ```

2. **HTTPS Required** - Must use HTTPS in production
   ```properties
   # Production
   API_BASE_URL=https://api.expensesense.com
   
   # Development
   API_BASE_URL=http://localhost:8000
   ```

---

## 📋 **Pre-Deployment Checklist**

### Backend Security
- [ ] Generate and set new `SECRET_KEY`
- [ ] Generate and set new `JWT_SECRET`
- [ ] Set specific `ALLOWED_HOSTS` (no wildcards)
- [ ] Set specific `CORS_ALLOWED_ORIGINS` (no wildcards)
- [ ] Verify `DEBUG=False`
- [ ] Add `.env` to `.gitignore`
- [ ] Enable HTTPS security headers
- [ ] Configure static files serving (WhiteNoise/S3)

### Database
- [ ] Verify RDS security group allows backend IP
- [ ] Test database connection from deployment server
- [ ] Run migrations on production DB
- [ ] Create database backups
- [ ] Set up automated backup schedule

### Frontend
- [ ] Update `API_BASE_URL` to production backend URL
- [ ] Ensure backend URL uses HTTPS
- [ ] Update Google OAuth redirect URIs in Google Console
- [ ] Add production domain to authorized domains

### Additional Security
- [ ] Set up SSL/TLS certificates (Let's Encrypt/ACM)
- [ ] Configure firewall rules
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up error tracking (Sentry)

---

## 🚀 **Deployment Steps**

### 1. Update Backend .env
```bash
cd backend

# Generate new keys
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
JWT_SECRET=$(python -c 'import secrets; print(secrets.token_urlsafe(64))')

# Edit .env with new values
nano .env
```

### 2. Update Frontend .env
```bash
cd frontend

# Update API URL
nano .env
# Change: API_BASE_URL=https://your-backend-url.com
```

### 3. Test Locally First
```bash
# Backend
cd backend
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver

# Frontend
cd frontend
flutter build web  # or build ios/android
```

### 4. Deploy to AWS

**Backend (EC2/ECS/Elastic Beanstalk)**:
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start with Gunicorn
gunicorn expensesense_backend.wsgi:application --bind 0.0.0.0:8000
```

**Frontend (S3/CloudFront/Netlify/Vercel)**:
```bash
flutter build web
# Deploy build/web folder
```

---

## 🔍 **Verify Deployment**

### Backend Health Check
```bash
curl https://your-backend-url.com/api/
```

### Test Endpoints
```bash
# Check API
curl https://your-backend-url.com/api/auth/register/ -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123456"}'
```

### Database Connection
```bash
python manage.py dbshell
# Should connect to RDS
```

---

## 📊 **Environment Files Summary**

### Backend .env Status
| Setting | Current | Production Ready | Priority |
|---------|---------|------------------|----------|
| DB Config | ✅ AWS RDS | ✅ Ready | - |
| SECRET_KEY | ❌ Dev Key | ❌ **CRITICAL** | 🔴 HIGH |
| JWT_SECRET | ❌ Dev Key | ❌ **CRITICAL** | 🔴 HIGH |
| DEBUG | ✅ False | ✅ Ready | - |
| ALLOWED_HOSTS | ❌ Wildcard | ❌ **CRITICAL** | 🔴 HIGH |
| CORS_ORIGINS | ❌ Wildcard | ❌ **CRITICAL** | 🔴 HIGH |

### Frontend .env Status
| Setting | Current | Production Ready | Priority |
|---------|---------|------------------|----------|
| API_BASE_URL | ❌ localhost | ❌ Update | 🟡 MEDIUM |
| GOOGLE_CLIENT_ID | ✅ Set | ✅ Ready | - |

---

## 🚨 **DO NOT DEPLOY WITHOUT FIXING:**

1. ❌ SECRET_KEY (using dev key)
2. ❌ JWT_SECRET (using dev key)
3. ❌ ALLOWED_HOSTS (wildcard)
4. ❌ CORS_ALLOWED_ORIGINS (wildcard)
5. ❌ Frontend API_BASE_URL (localhost)

---

## 📞 **Need Help?**

Check these files:
- `backend/expensesense_backend/settings.py` - Django settings
- `backend/.env` - Environment variables
- `frontend/.env` - Frontend config

Run security check:
```bash
cd backend
python manage.py check --deploy
```

---

## ✅ **Ready to Deploy When:**

- [ ] All SECRET keys generated and updated
- [ ] ALLOWED_HOSTS set to specific domains
- [ ] CORS origins set to specific domains
- [ ] Frontend API_BASE_URL points to production
- [ ] HTTPS enabled on both frontend and backend
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] All tests passing
- [ ] Security check passes (`python manage.py check --deploy`)

---

**Current Status**: 🔴 **NOT READY FOR PRODUCTION**

**Critical Issues**: 5 security issues must be fixed

**Estimated Time to Fix**: 15-30 minutes
