# Rest API development using djangorestapi  

## 1. Install Python libraries
#### 1) Install Python 3.x
#### 2) pip install -r requirements  
#### 3) python manage.py runserver

## 2. Database
#### PostgreSQL
- Database name: 'blog'
- User: 'postgres'
- Password: '1234'
- Host: '127.0.0.1'
- Port: '5432'
#### Database Structure
- auth_user table: (username, email password)
- blog_question table: (title, slug, content, created_at, user_id, height_field, image, width_field)
- blog_answer table: (object_id, content, timestamp, content_type_id, parent_id, user_id)

## 3. Rest API Guide
#### 1) Authentication
- Login: 
http://127.0.0.1:8000/blog/users/login/
- Register: 
http://127.0.0.1:8000/blog/users/register/

#### 2) Question api
- Post question: 
http://127.0.0.1:8000/blog/questions/create/
- Question detail: 
http://127.0.0.1:8000/blog/questions/id/
- Edit question: 
http://127.0.0.1:8000/blog/questions/id/edit/
- Delete question: 
http://127.0.0.1:8000/blog/questions/id/delete/
- View questions: 
http://127.0.0.1:8000/blog/questions/

#### 3) Answer api
- Post answer: 
http://127.0.0.1:8000/blog/answers/create/
- Answer detail: 
http://127.0.0.1:8000/blog/answers/id/
- View answers: 
http://127.0.0.1:8000/blog/answers/

#### 4) Bookmark for Question and Answer
- Question: 
http://127.0.0.1:8000/blog/questions/id/  
This link includes url for each question. so you can use this url to bookmark.
- Answer: 
http://127.0.0.1:8000/blog/answers/id/  
This link includes url for each answer. so you can use this url to bookmark.  

## 3. Unit Test
Use Postman or Django REST framework to do unit tests.
- If click each link, you can directly do unit test in Django REST framework Panel.  
https://github.com/jesus9233/blog-rest-api/blob/master/media/images/DRF.PNG
- If prefer Postman, reference Postman API document.
