# ⚡ QUICKSTART GUIDE - ExpenseSense

Get your ExpenseSense app running in **5 minutes**!

---

## 🎯 **OPTION 1: Quick Local Setup (No Docker)**

### **Backend Setup (3 minutes)**

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env

# 5. Edit .env (minimal required):
# DB_NAME=expensesense_db
# DB_USER=root
# DB_PASSWORD=yourpassword
# SECRET_KEY=your-secret-key
# GOOGLE_CLIENT_ID=your-google-client-id

# 6. Create MySQL database
mysql -u root -p
> CREATE DATABASE expensesense_db;
> EXIT;

# 7. Run migrations
python manage.py migrate

# 8. Create admin user
python manage.py createsuperuser

# 9. Train ML model (optional - takes 2-3 minutes)
cd ml_model && python train_model.py && cd ..

# 10. Start server
python manage.py runserver
```

✅ **Backend running at http://localhost:8000**

---

### **Frontend Setup (2 minutes)**

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
flutter pub get

# 3. Setup environment
cp .env.example .env

# 4. Edit .env:
# API_BASE_URL=http://localhost:8000
# GOOGLE_CLIENT_ID=your-google-client-id

# 5. Run app
flutter run

# For Android emulator, use:
# API_BASE_URL=http://10.0.2.2:8000

# For real device, use your computer's IP:
# API_BASE_URL=http://192.168.1.X:8000
```

✅ **App running on your emulator/device**

---

## 🐳 **OPTION 2: Docker Setup (Even Faster!)**

```bash
# 1. Navigate to backend
cd backend

# 2. Setup environment
cp .env.example .env

# 3. Edit .env with your settings

# 4. Build and run
docker-compose up --build
```

✅ **Backend + MySQL running at http://localhost:8000**

Then follow frontend setup from Option 1.

---

## 🧪 **TEST THE API**

### **1. Register a User**
```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

### **2. Login**
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Save the `access` token from response.

### **3. Create Expense**
```bash
curl -X POST http://localhost:8000/expenses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "amount": 500,
    "merchant": "Starbucks",
    "category": "food",
    "payment_mode": "card",
    "date": "2024-10-27T10:00:00Z",
    "notes": "Morning coffee"
  }'
```

### **4. Test ML Classification**
```bash
curl -X POST http://localhost:8000/ml/classify/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "sms_text": "Spent Rs 500 at McDonald's"
  }'
```

---

## 🔑 **GOOGLE OAUTH SETUP (Optional)**

1. Go to https://console.cloud.google.com/
2. Create project → APIs & Services → Credentials
3. Create OAuth 2.0 Client ID (Web application)
4. Add to `.env`:
   - Backend: `GOOGLE_CLIENT_ID=xxx`
   - Frontend: `GOOGLE_CLIENT_ID=xxx`

---

## 📱 **MOBILE APP SCREENS**

After running `flutter run`, you'll see:
1. **Splash Screen** → Checks authentication
2. **Login Screen** → Email/password + Google Sign-In
3. **Dashboard** → Monthly summary & categories
4. **Expenses List** → View all transactions
5. **Add Expense** → Manual entry
6. **Profile** → User details + logout

---

## 🚨 **COMMON ISSUES**

### **"Connection refused" in Flutter**
- **Android Emulator**: Use `http://10.0.2.2:8000`
- **iOS Simulator**: Use `http://localhost:8000`
- **Real Device**: Use your computer's IP (e.g., `http://192.168.1.5:8000`)

### **MySQL connection error**
```bash
# Make sure MySQL is running
mysql --version
# Check if database exists
mysql -u root -p -e "SHOW DATABASES;"
```

### **Flutter package errors**
```bash
flutter clean
flutter pub get
flutter run
```

### **PyTorch not using MPS (Apple Silicon)**
```python
# Check in Python:
import torch
print(torch.backends.mps.is_available())  # Should be True
```

---

## 📚 **NEXT STEPS**

1. ✅ **Customize Categories**: Edit `expenses/models.py`
2. ✅ **Train with Real Data**: Replace sample data in `train_model.py`
3. ✅ **Add Charts**: Implement charts in Flutter dashboard
4. ✅ **SMS Permission**: Add SMS reading for auto-classification
5. ✅ **Deploy**: Follow deployment guide in main README

---

## 🎉 **YOU'RE ALL SET!**

Your ExpenseSense app is now running!

- **Backend Admin**: http://localhost:8000/admin/
- **API Docs**: Test endpoints using Postman or curl
- **Mobile App**: Running on your emulator/device

**Happy Expense Tracking! 💰**
