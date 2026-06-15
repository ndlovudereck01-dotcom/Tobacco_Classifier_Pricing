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
   # 1. Download the miniconda installer
      Linux (64-bit):
         wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
 
      macOS (Intel):
         wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
 
      macOS (Apple Silicon M1/M2):
         wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
 
      Windows:
        Download from: https://docs.conda.io/en/latest/miniconda.html
        Run the .exe installer and follow the GUI wizard.
 
  # 2. Make the script executable (Linux/macOS only)
    chmod +x Miniconda3-latest-Linux-x86_64.sh
  
  # 3. Run the installer
    bash Miniconda3-latest-Linux-x86_64.sh
     
  # 4. Create environment
    conda create --name tobacco-env python=3.11
 
  # 5. Activate it
    conda activate tobacco-env
 
  # 6. Navigate to project
    cd /home/youruser/your_project(Tobacco_Classifier_Pricing) # project path
 
  # 7. Install dependencies
    pip install -r requirements.txt
 
  # 8. Apply migrations
    python manage.py migrate
 
  # 9. Collect static files
    python manage.py collectstatic
 
  # 10. Run dev server to test
    python manage.py runserver
 
  # 11. Install gunicorn (if not in requirements.txt)
    pip install gunicorn
 
  # 9. Test gunicorn manually
    gunicorn --workers 3 --bind 0.0.0.0:8000 your_project.wsgi:application
 
