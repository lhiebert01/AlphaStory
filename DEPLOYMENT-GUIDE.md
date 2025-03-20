# Deployment Guide for Alphabet Adventure App

This guide provides instructions for deploying the Alphabet Adventure app to different platforms.

## Table of Contents
- [GitHub Deployment](#github-deployment)
- [Render Deployment](#render-deployment)
- [Local Deployment](#local-deployment)
- [Environment Variables](#environment-variables)
- [Future Enhancements](#future-enhancements)

## GitHub Deployment

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click "New" to create a new repository
3. Name it `alphabet-adventure-app`
4. Add a description (optional)
5. Choose visibility (public or private)
6. Click "Create repository"

### 2. Initialize and Push Your Local Repository

```bash
# Navigate to project directory
cd C:\src\storywriter2

# Initialize Git repository
git init

# Add .gitignore first
git add .gitignore
git commit -m "Add .gitignore"

# Add essential files
git add README.md requirements.txt render.yaml
git add .streamlit/
git add alphabet_book_streamlit_app11.py dual_voice_generator.py
git add DEPLOYMENT-GUIDE.md
git add alphabet_stories_new/ alphabet_images_new/ alphabet_images_new_illustrations/ alphabet_audio_files/

# Commit files
git commit -m "Initial commit - Alphabet Adventure App"

# Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/alphabet-adventure-app.git

# Push to GitHub
git push -u origin main
```

## Render Deployment

### 1. Manual Deployment via Dashboard
1. Create an account at [render.com](https://render.com)
2. Go to Dashboard and click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure as follows:
   - **Name**: `alphabet-adventure`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run alphabet_book_streamlit_app11.py`
5. Set environment variables (see [Environment Variables](#environment-variables))
6. Click "Create Web Service"

### 2. Automatic Deployment via render.yaml
1. Ensure `render.yaml` is in your repository root
2. Go to Render Dashboard
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will detect the YAML file and configure services automatically
6. Add your environment secrets manually
7. Deploy

## Local Deployment

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/alphabet-adventure-app.git
cd alphabet-adventure-app
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` File
Create a file named `.env` in the project root with:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json
```

### 4. Run Application
```bash
streamlit run alphabet_book_streamlit_app11.py
```

## Environment Variables

These variables need to be set for deployment:

| Variable | Description | Required? |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | OpenAI API key for the chatbot functionality | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google Cloud credentials for TTS | Yes |

### Setting Up Google Cloud Text-to-Speech
1. Create a Google Cloud project
2. Enable the Text-to-Speech API
3. Create a service account with "Cloud Text-to-Speech User" role
4. Download the JSON key file
5. For Render: 
   - Go to Dashboard → Your Service → Environment
   - Add the contents of the JSON file as a secret

## Future Enhancements

### Database Integration
1. Set up PostgreSQL on Render
2. Add SQLAlchemy and database models
3. Implement user authentication tables

### Payment Processing
1. Set up Stripe integration
2. Create webhook endpoint
3. Implement subscription models

### Gumroad Integration
1. Set up Gumroad API client
2. Create digital product listings
3. Implement license verification

---

For additional assistance, contact [Lindsay Hiebert](https://www.linkedin.com/in/lindsayhiebert/).