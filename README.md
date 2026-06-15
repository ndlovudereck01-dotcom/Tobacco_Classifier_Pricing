# Tobacco Classifier & Pricing System

A Django web application that classifies tobacco leaf quality and estimates pricing
using machine learning.

## Features
- Tobacco grade classification
- Automated pricing engine
- REST API with Django REST Framework
- Deployed with Gunicorn + Nginx

## Tech Stack
- Python 3.x, Django, Gunicorn
- Anaconda (Miniconda3)
- PostgreSQL / SQLite
- GitHub Actions CI/CD

## Setup 
### environment setup (using miniconda(anaconda))
----------------------------------------------------------------
  # 1. Create environment
  conda create --name tobacco-env python=3.11
 
  # 2. Activate it
  conda activate tobacco-env
 
  # 3. Navigate to project
  cd /home/youruser/Desktop/Tobacco_Classifier_Pricing # project path
 
  # 4. Install dependencies
  pip install -r requirements.txt
 
  # 5. Apply migrations
  python manage.py migrate
 
  # 6. Collect static files
  python manage.py collectstatic
 
  # 7. Run dev server to test
  python manage.py runserver
 
  # 8. Install gunicorn (if not in requirements.txt)
  pip install gunicorn
 
  # 9. Test gunicorn manually
  gunicorn --workers 3 --bind 0.0.0.0:8000 your_project.wsgi:application
 
