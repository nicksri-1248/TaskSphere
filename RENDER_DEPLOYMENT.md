# 🚀 Deploy TaskSphere to Render

## Step-by-Step Render Deployment Guide

### Prerequisites ✅
- ✅ GitHub account with TaskSphere repository
- ✅ All configuration files committed and pushed
- ✅ Project ready for deployment

### Step 1: Create Render Account
1. **Go to**: https://render.com/
2. **Sign up** with your GitHub account (recommended)
3. **Authorize Render** to access your GitHub repositories

### Step 2: Create PostgreSQL Database
1. **Click "New +"** in Render dashboard
2. **Select "PostgreSQL"**
3. **Configure database**:
   - **Name**: `tasksphere-db`
   - **Database**: `tasksphere`
   - **User**: `tasksphere`
   - **Region**: Choose closest to you (e.g., Oregon)
   - **PostgreSQL Version**: Latest
   - **Plan**: **Free** (perfect for development)
4. **Click "Create Database"**
5. **Wait for database** to be created (takes 1-2 minutes)
6. **Copy the Internal Database URL** (you'll need this)

### Step 3: Create Web Service
1. **Click "New +"** again
2. **Select "Web Service"**
3. **Connect Repository**: Select your `TaskSphere` repository
4. **Configure Web Service**:
   - **Name**: `tasksphere-web`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn manager.wsgi:application`
   - **Plan**: **Free** (great for testing)

### Step 4: Environment Variables
In the **Environment Variables** section, add these:

```
SECRET_KEY = [Click "Generate"] (Render will auto-generate a secure key)
DEBUG = False
DJANGO_SETTINGS_MODULE = manager.settings
WEB_CONCURRENCY = 4
```

### Step 5: Connect Database
1. **Add Environment Variable**:
   - **Key**: `DATABASE_URL`
   - **Value**: Select your PostgreSQL database from the dropdown
   - This automatically connects your web service to the database

### Step 6: Deploy! 🎉
1. **Click "Create Web Service"**
2. **Render will automatically**:
   - Clone your repository
   - Install dependencies from requirements.txt
   - Run the build script (migrations, collectstatic)
   - Start your Django application
3. **Monitor deployment** in the build logs
4. **Deployment takes** 3-5 minutes

### Step 7: Post-Deployment Setup
Once deployed successfully:

1. **Create Superuser**:
   - Go to your web service dashboard
   - Click **"Shell"** tab
   - Run: `python manage.py createsuperuser`
   - Follow the prompts to create admin account

2. **Test Your Application**:
   - Visit your app URL: `https://tasksphere-web.onrender.com`
   - Login with superuser credentials
   - Test creating projects and tasks

## 🎯 Your App URLs
- **Live App**: `https://tasksphere-web.onrender.com`
- **Admin Panel**: `https://tasksphere-web.onrender.com/admin/`
- **Render Dashboard**: https://dashboard.render.com/

## 🔧 Troubleshooting

### Common Issues:
1. **Build Failed**: Check build logs for specific errors
2. **Database Connection**: Ensure DATABASE_URL is properly connected
3. **Static Files**: Build script handles this automatically
4. **Environment Variables**: Double-check all required vars are set

### Useful Commands in Render Shell:
```bash
# Check Django setup
python manage.py check --deploy

# Create superuser
python manage.py createsuperuser

# Run custom commands
python manage.py shell

# View database tables
python manage.py dbshell
```

## 📊 Render Free Tier Limits
- **750 hours/month** (enough for 24/7 operation)
- **512 MB RAM**
- **0.1 CPU**
- **Free PostgreSQL database**
- **Automatic HTTPS**
- **Custom domains** (free)

## 🎉 Next Steps After Deployment
1. **Test all functionality** thoroughly
2. **Set up monitoring** (Render provides built-in monitoring)
3. **Configure custom domain** (optional)
4. **Set up environment-specific settings**
5. **Monitor usage** and upgrade if needed

## 📁 Files Created for Render
- ✅ `build.sh` - Build script for deployment
- ✅ `render.yaml` - Render service configuration
- ✅ Updated `settings.py` - Render-specific configurations
- ✅ All existing Heroku files work with Render too!

Your Django Project Management System is now ready to go live on Render! 🚀