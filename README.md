# 💰 ExpenseSense - AI-Powered Expense Tracking App

ExpenseSense is a full-stack mobile application that helps users track their expenses with **AI-powered SMS classification** using a CNN model. The app features **Django REST API** backend, **Flutter** mobile frontend, **JWT authentication**, **Google OAuth**, and **Machine Learning** for automatic expense categorization.

---

## 🏗️ **PROJECT STRUCTURE**

```
ExpenseSense/
├── backend/                    # Django REST API + ML Model
│   ├── expensesense_backend/   # Django project settings
│   ├── users/                  # Authentication app (Email + Google OAuth)
│   ├── expenses/               # Expense CRUD app
│   ├── ml_model/               # CNN Model for SMS classification
│   ├── Dockerfile              # Docker configuration
│   ├── docker-compose.yml      # Docker Compose with MySQL
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
│
├── frontend/                   # Flutter mobile app
│   ├── lib/
│   │   ├── models/             # Data models
│   │   ├── providers/          # State management (Provider)
│   │   ├── screens/            # UI screens
│   │   ├── services/           # API service layer
│   │   └── main.dart           # App entry point
│   ├── assets/                 # Images and icons
│   ├── pubspec.yaml            # Flutter dependencies
│   └── .env.example            # Environment variables template
│
└── README.md                   # This file
```

---

## 🚀 **FEATURES**

### **Authentication**
- ✅ Email/Password Registration & Login
- ✅ Google OAuth 2.0 Sign-In
- ✅ JWT Token Authentication (Access + Refresh)
- ✅ Persistent Login (Secure Storage)

### **Expense Management**
- ✅ Create, Read, Update, Delete Expenses
- ✅ Filter by Category, Date Range, Payment Mode
- ✅ Monthly & Yearly Expense Summaries
- ✅ Category-wise Breakdown with Percentages

### **AI-Powered Classification**
- ✅ CNN Model trained on SMS expense data
- ✅ Automatic category prediction from SMS text
- ✅ Supports 10 categories: Food, Transport, Shopping, Entertainment, Bills, Healthcare, Education, Groceries, Travel, Other
- ✅ Trained on Apple Silicon (MPS) for M1/M2/M3 Macs

### **Mobile App (Flutter)**
- ✅ Cross-platform (Android & iOS)
- ✅ Material Design 3
- ✅ Dark Mode Support
- ✅ Responsive UI
- ✅ Charts & Visualizations

---

## 🛠️ **TECH STACK**

### **Backend**
- **Framework**: Django 5.x + Django REST Framework
- **Database**: MySQL 8.0 (AWS RDS Compatible)
- **Authentication**: Simple JWT + Google OAuth2
- **ML Framework**: PyTorch (with MPS support for Apple Silicon)
- **Server**: Gunicorn
- **Static Files**: WhiteNoise
- **CORS**: django-cors-headers

### **Frontend**
- **Framework**: Flutter 3.x (Dart 3.x)
- **State Management**: Provider
- **HTTP Client**: Dio
- **Secure Storage**: flutter_secure_storage
- **OAuth**: google_sign_in
- **Charts**: fl_chart

### **DevOps**
- **Containerization**: Docker + Docker Compose
- **Database**: MySQL 8.0
- **Deployment Ready**: AWS EC2, RDS, S3

---

## 📦 **INSTALLATION & SETUP**

### **Prerequisites**
- Python 3.10+
- MySQL 8.0+
- Flutter 3.0+ with Dart 3.0+
- Docker & Docker Compose (optional)
- PyTorch (for ML model training)

---

## 🔧 **BACKEND SETUP**

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd ExpenseSense/backend
```

### **2. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# Database
DB_NAME=expensesense_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET=your-jwt-secret-key

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### **5. Create MySQL Database**
```bash
mysql -u root -p
CREATE DATABASE expensesense_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### **6. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **7. Create Superuser**
```bash
python manage.py createsuperuser
```

### **8. Train ML Model (Optional - Apple Silicon)**
```bash
cd ml_model
python train_model.py
```

This will train the CNN model on Apple Silicon (MPS) and save it as `expense_cnn_model.pt`.

### **9. Run Development Server**
```bash
python manage.py runserver
```

Backend API will be available at: **http://localhost:8000**

---

## 🐳 **BACKEND - DOCKER DEPLOYMENT**

### **1. Using Docker Compose (Recommended)**
```bash
cd backend

# Copy environment file
cp .env.example .env

# Edit .env with your configuration

# Build and run
docker-compose up --build
```

Services:
- **Backend API**: http://localhost:8000
- **MySQL Database**: localhost:3306

### **2. Stop Services**
```bash
docker-compose down
```

### **3. View Logs**
```bash
docker-compose logs -f backend
```

---

## 📱 **FRONTEND SETUP (Flutter)**

### **1. Navigate to Frontend Directory**
```bash
cd frontend
```

### **2. Install Dependencies**
```bash
flutter pub get
```

### **3. Configure Environment**
```bash
cp .env.example .env
```

Edit `.env`:
```bash
# API Configuration
API_BASE_URL=http://localhost:8000

# For Android Emulator
# API_BASE_URL=http://10.0.2.2:8000

# For iOS Simulator
# API_BASE_URL=http://localhost:8000

# For Real Device (replace with your computer's IP)
# API_BASE_URL=http://192.168.1.X:8000

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

### **4. Run the App**

**For Android Emulator:**
```bash
flutter run
```

**For iOS Simulator:**
```bash
flutter run -d ios
```

**For Web:**
```bash
flutter run -d chrome
```

---

## 🔑 **API ENDPOINTS**

### **Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register new user |
| POST | `/auth/login/` | Login with email/password |
| POST | `/auth/google/` | Google OAuth login |
| POST | `/auth/token/refresh/` | Refresh access token |
| GET | `/auth/profile/` | Get user profile |

### **Expenses**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses/` | List all expenses |
| POST | `/expenses/` | Create expense |
| GET | `/expenses/{id}/` | Get specific expense |
| PUT | `/expenses/{id}/` | Update expense |
| DELETE | `/expenses/{id}/` | Delete expense |
| GET | `/expenses/summary/monthly/` | Monthly summary |
| GET | `/expenses/summary/yearly/` | Yearly summary |

### **ML Classification**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ml/classify/` | Classify SMS expense |

---

## 🤖 **ML MODEL TRAINING**

The CNN model is trained on Apple Silicon (M1/M2/M3) using **MPS acceleration**.

### **Training Script**
```bash
cd backend/ml_model
python train_model.py
```

### **Model Architecture**
- **Input**: SMS text (preprocessed and tokenized)
- **Embedding Layer**: 10,000 vocab size, 128 dimensions
- **3 Convolutional Layers**: Different kernel sizes (3, 4, 5)
- **Global Max Pooling**
- **Fully Connected Layers**: 384 → 64 → 10
- **Output**: 10 categories

### **Categories**
1. Food & Dining
2. Transportation
3. Shopping
4. Entertainment
5. Bills & Utilities
6. Healthcare
7. Education
8. Groceries
9. Travel
10. Other

---

## 🌐 **GOOGLE OAUTH SETUP**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google+ API**
4. Create OAuth 2.0 credentials:
   - **Application Type**: Web application
   - **Authorized redirect URIs**: `http://localhost:8000` (for testing)
5. Copy **Client ID** and **Client Secret**
6. Add Client ID to both backend and frontend `.env` files

---

## 📊 **DATABASE SCHEMA**

### **Users Table**
```sql
id, username, email, password, google_id, date_joined, is_active, is_staff
```

### **Expenses Table**
```sql
id, user_id, amount, merchant, category, payment_mode, 
date, sms_raw_text, notes, created_at, updated_at
```

---

## 🚀 **DEPLOYMENT GUIDE**

### **Backend - AWS EC2**
1. Launch Ubuntu 22.04 EC2 instance
2. Install Docker & Docker Compose
3. Clone repository
4. Configure `.env` with production settings
5. Set up AWS RDS for MySQL
6. Run `docker-compose up -d`
7. Configure NGINX as reverse proxy
8. Set up SSL with Let's Encrypt

### **Frontend - Build APK/IPA**

**Android:**
```bash
flutter build apk --release
# APK located at: build/app/outputs/flutter-apk/app-release.apk
```

**iOS:**
```bash
flutter build ios --release
# Archive with Xcode for App Store
```

---

## 🧪 **TESTING**

### **Backend Tests**
```bash
cd backend
python manage.py test
```

### **Flutter Tests**
```bash
cd frontend
flutter test
```

---

## 📝 **LICENSE**

This project is licensed under the MIT License.

---

## 👨‍💻 **DEVELOPER**

**Arvin Samuela**
- VIT University - CAD Project
- Full-Stack Developer specializing in Django, Flutter, ML

---

## 🤝 **CONTRIBUTING**

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📧 **SUPPORT**

For issues or questions, please open a GitHub issue or contact the developer.

---

## 🎉 **ACKNOWLEDGMENTS**

- Django & Django REST Framework
- Flutter Team
- PyTorch Team
- Google Cloud Platform
- MySQL Community

---

**Built with ❤️ using Django, Flutter, and PyTorch on Apple Silicon**
