# Quick Start Guide

## How to Run the Secure Vault Project

### Option 1: Automated Setup (Easiest)

1. **Open terminal/command prompt in project folder**

2. **Run setup script:**
   ```bash
   # Windows:
   setup.bat
   
   # macOS/Linux:
   ./setup.sh
   ```

3. **Follow the instructions displayed**

### Option 2: Manual Setup

#### Step 1: Backend Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt
```

#### Step 2: Start Backend
```bash
# From project root directory (with venv activated)
python api/main.py
```
✅ Backend runs at: http://localhost:8080

#### Step 3: Start Frontend (New Terminal)
```bash
# From project root directory
cd frontend-react
npm install
npm start
```
✅ Frontend runs at: http://localhost:3000

## What You Should See

1. **Backend Terminal:** "Uvicorn running on http://127.0.0.1:8080"
2. **Frontend Terminal:** "webpack compiled successfully"
3. **Browser:** Login page opens automatically at localhost:3000

## Quick Test

1. **Register:** Create account (username + password 8+ chars)
2. **Login:** Use your credentials
3. **Add Entry:** Create a password entry for a service
4. **Success!** You now have a working password manager

## Troubleshooting

- **Port in use?** Kill processes or change ports
- **Module not found?** Check virtual environment is activated
- **Can't connect?** Ensure both backend and frontend are running

## Important URLs

- **App:** http://localhost:3000
- **API:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs

Need help? Check the full README.md for detailed troubleshooting.
