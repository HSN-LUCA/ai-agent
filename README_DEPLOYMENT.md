# LogX - Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud

### Step 1: Prepare Repository
1. Create GitHub repository
2. Push all files except sensitive data (.env, secrets)

### Step 2: Streamlit Cloud Setup
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your LogX repository
4. Set main file: `app.py`

### Step 3: Configure Secrets
In Streamlit Cloud dashboard, add these secrets:

```toml
[secrets]
OPENAI_API_KEY = "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"

# Optional: SQL Server credentials
SQL_SERVER = "your-server-name"
SQL_DATABASE = "your-database-name"
SQL_USERNAME = "your-username"
SQL_PASSWORD = "your-password"
```

### Step 4: Deploy
- Click "Deploy" button
- App will be available at: `https://your-app-name.streamlit.app`

## 🔧 Local Development
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Features
- Natural language to SQL queries
- Interactive charts and visualizations
- Chat history with tabs
- Database connectivity (SQLite/SQL Server)
- Logo upload and branding

## 🛠️ Tech Stack
- Streamlit (UI)
- LangChain (AI/SQL)
- OpenAI GPT-3.5 (Language Model)
- Plotly (Charts)
- SQLAlchemy (Database)