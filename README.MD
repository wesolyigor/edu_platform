# Edu Platoform

Django App to create and make online courses

### Requirements and technical details:

- Base: 
  - Python 3.9
  - Django 3.1.6
    - User authentication by ```django.allauth 0.43```
    - Django Templates
      - Separate and independence elements of views
    - Forms:
      - `django-crispy-forms 1.11`
    
    
- Containerization
    - Docker 
    - Docker Compose
- DB
  - Postgres
    - Psycopg2-binary 2.8.6 (necessary package)

Additional
- Images:
  - Pillow 8.1.1
  

## Start:

- git clone git@github.com:wesolyigor/edu_platform.git
- Pipenv install
- sudo docker-compose up --build 

### in second terminal:

(migration)
- sudo docker-compose exec backend python manage.py makemigrations 
- sudo docker-compose exec backend python manage.py migrate

_(create group of users)_

- sudo docker-compose exec backend python manage.py shell
- from users.models import *
- a = Group.objects.create(name="instructor")
- b = Group.objects.create(name="student")
- a.save()
- b.save()


_(create subject of course)_
- sudo docker-compose exec backend python manage.py shell
- from courses.models import *
- s = Subject.objects.create(title="temp")
- s.save()
- exit()

(create superuser)

- sudo docker-compose exec backend python manage.py createsuperuser

_(to stop):_ 

- ctrl + C

_(to remove image and clean base:)_
- sudo docker-compose down 

