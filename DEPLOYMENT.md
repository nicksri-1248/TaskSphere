# Heroku Deployment Guide

## Prerequisites
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create a Heroku account: https://signup.heroku.com/

## Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create a new Heroku app
```bash
heroku create your-app-name-here
```

### 3. Add PostgreSQL database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 4. Set environment variables
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=manager.settings
```

### 5. Initialize Git repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 6. Add Heroku remote
```bash
heroku git:remote -a your-app-name-here
```

### 7. Deploy to Heroku
```bash
git push heroku main
```

### 8. Run migrations on Heroku
```bash
heroku run python manage.py migrate
```

### 9. Create superuser (optional)
```bash
heroku run python manage.py createsuperuser
```

### 10. Collect static files (if needed)
```bash
heroku run python manage.py collectstatic --noinput
```

## Troubleshooting

### Check logs
```bash
heroku logs --tail
```

### Check config vars
```bash
heroku config
```

### Run Django commands on Heroku
```bash
heroku run python manage.py shell
heroku run python manage.py dbshell
```

## Important Notes

1. **Static Files**: Using WhiteNoise for static file serving (no S3 setup required)
2. **Database**: PostgreSQL is automatically configured via DATABASE_URL
3. **Security**: DEBUG is set to False in production
4. **Logging**: Configured to output to Heroku logs

## Optional AWS S3 Setup
If you want to use AWS S3 for static/media files:
1. Uncomment the S3 configuration in settings.py
2. Set these environment variables:
```bash
heroku config:set AWS_ACCESS_KEY_ID="your-key"
heroku config:set AWS_SECRET_ACCESS_KEY="your-secret"
heroku config:set AWS_STORAGE_BUCKET_NAME="your-bucket"
```

## Files Created/Modified for Deployment
- `requirements.txt` - Updated with production dependencies
- `Procfile` - Defines how to run the app on Heroku
- `runtime.txt` - Specifies Python version (3.11.10)
- `manager/settings.py` - Updated with production configuration
- `.env.example` - Template for environment variables