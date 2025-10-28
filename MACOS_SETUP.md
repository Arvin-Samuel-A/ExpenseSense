# 🚀 MacOS Setup Guide for ExpenseSense

This guide is specifically for **macOS** users (especially Apple Silicon M1/M2/M3).

---

## 📋 **PREREQUISITES**

### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Required System Dependencies
```bash
# Install MySQL and pkg-config
brew install mysql pkg-config

# Start MySQL service
brew services start mysql

# Secure MySQL installation (optional but recommended)
mysql_secure_installation
```

### 3. Install Python 3.9+ (if needed)
```bash
# Check Python version
python3 --version

# If needed, install Python
brew install python@3.9
```

### 4. Install Flutter
```bash
# Using Homebrew
brew install --cask flutter

# OR download from: https://flutter.dev/docs/get-started/install/macos

# Verify installation
flutter doctor
```

---

## 🔧 **BACKEND SETUP (macOS)**

### Step 1: Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Note**: If you get `mysqlclient` installation errors, run:
```bash
brew install mysql pkg-config
export LDFLAGS="-L/opt/homebrew/opt/mysql/lib"
export CPPFLAGS="-I/opt/homebrew/opt/mysql/include"
pip install mysqlclient
```

### Step 3: Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your settings
```

Minimum required in `.env`:
```bash
DB_NAME=expensesense_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
```

### Step 4: Setup MySQL Database
```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE expensesense_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Train ML Model (Optional - Uses Apple Silicon MPS)
```bash
cd ml_model
python train_model.py
cd ..
```

This will use **Apple Silicon MPS acceleration** automatically!

### Step 8: Start Development Server
```bash
python manage.py runserver
```

✅ Backend running at: **http://localhost:8000**

---

## 📱 **FRONTEND SETUP (macOS)**

### Step 1: Get Dependencies
```bash
cd frontend
flutter pub get
```

### Step 2: Configure Environment
```bash
cp .env.example .env
```

Edit `.env`:
```bash
# For iOS Simulator (localhost works)
API_BASE_URL=http://localhost:8000

# For Android Emulator (use special IP)
# API_BASE_URL=http://10.0.2.2:8000

# For Real Device (use your Mac's IP)
# Find IP: ifconfig | grep "inet " | grep -v 127.0.0.1
# API_BASE_URL=http://192.168.1.XXX:8000

GOOGLE_CLIENT_ID=your-google-client-id
```

### Step 3: Run on iOS Simulator
```bash
# Open iOS simulator
open -a Simulator

# Run app
flutter run -d ios
```

### Step 4: Run on Android Emulator
```bash
# List devices
flutter devices

# Run on Android
flutter run -d android
```

---

## 🧪 **TEST THE SETUP**

### Test Backend API
```bash
cd backend
source venv/bin/activate
python test_api.py
```

### Test Flutter App
1. Launch simulator/emulator
2. Run `flutter run`
3. Register a new user
4. Login and view dashboard

---

## 🐳 **ALTERNATIVE: DOCKER SETUP (Easier)**

If you prefer Docker (no need for manual MySQL setup):

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env with your settings
docker-compose up --build
```

This will start both Django backend and MySQL database!

---

## 🔧 **COMMON MACOS ISSUES & FIXES**

### Issue 1: `mysqlclient` won't install
```bash
brew install mysql pkg-config
export LDFLAGS="-L/opt/homebrew/opt/mysql/lib"
export CPPFLAGS="-I/opt/homebrew/opt/mysql/include"
pip install mysqlclient
```

### Issue 2: PyTorch not using MPS
```python
# Check in Python:
import torch
print(torch.backends.mps.is_available())  # Should return True
print(torch.backends.mps.is_built())      # Should return True

# If False, reinstall PyTorch:
pip uninstall torch torchvision
pip install torch torchvision
```

### Issue 3: MySQL not starting
```bash
brew services restart mysql
brew services list  # Check status
```

### Issue 4: Flutter iOS build fails
```bash
cd ios
pod install
cd ..
flutter clean
flutter pub get
flutter run -d ios
```

### Issue 5: Android SDK not found
```bash
# Install Android Studio from: https://developer.android.com/studio
# Then run:
flutter doctor --android-licenses
flutter doctor
```

### Issue 6: Cannot connect to backend from device
```bash
# Find your Mac's IP:
ifconfig | grep "inet " | grep -v 127.0.0.1

# Use that IP in Flutter .env:
API_BASE_URL=http://192.168.1.XXX:8000

# Make sure firewall allows connections:
# System Preferences → Security & Privacy → Firewall → Allow Django
```

---

## 🎯 **QUICK START COMMANDS**

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### Terminal 2 - Frontend
```bash
cd frontend
flutter run
```

---

## ✅ **VERIFICATION CHECKLIST**

- [ ] Python 3.9+ installed
- [ ] MySQL installed and running
- [ ] pkg-config installed
- [ ] Virtual environment created
- [ ] Dependencies installed successfully
- [ ] .env files configured
- [ ] Database created
- [ ] Migrations run
- [ ] Superuser created
- [ ] Backend server starts without errors
- [ ] Flutter dependencies installed
- [ ] Flutter app runs on simulator/emulator
- [ ] Can register and login
- [ ] Can create expenses

---

## 📊 **SYSTEM REQUIREMENTS**

- **macOS**: 11.0 (Big Sur) or later
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Xcode**: Latest version (for iOS development)
- **Android Studio**: Latest (for Android development)

---

## 🎉 **SUCCESS!**

If everything works, you should see:
- Backend API at http://localhost:8000
- Admin panel at http://localhost:8000/admin/
- Flutter app running on your simulator/emulator

**Happy Coding on macOS! 🍎**
