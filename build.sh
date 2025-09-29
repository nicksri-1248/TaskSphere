#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Django 3.2.25 deployment build..."

# Upgrade pip to latest version
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Check Django installation
echo "✅ Verifying Django installation..."
python -c "import django; print(f'Django {django.get_version()} installed successfully')"

# Run system checks
echo "🔍 Running Django system checks..."
python manage.py check --deploy

# Run migrations
echo "🗃️ Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🎉 Build completed successfully!"