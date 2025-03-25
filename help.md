cd src && docker-compose up --build

curl -X GET "http://localhost:5000/user?username=testuser"

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass", "email": "testemail@example.com"}' \
http://localhost:5000/register

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "email": "testemail@example.com"}' \
http://localhost:5000/register

curl -X PATCH -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "phone_number": "8800553535"}' \
http://localhost:5000/update_profile

curl -X PATCH -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "birth_date": "2003-07-01"}' \
http://localhost:5000/update_profile

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "title": "one two", "description": "privet"}' \
http://localhost:5000/create_post

curl -X GET -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "id": 4}' \
http://localhost:5000/get_post

curl -X PATCH -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "id": 4, "tags": ["tag1", "tag2"]}' \
http://localhost:5000/update_post

curl -X GET -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "page_number": 0, "page_size": 10, "author": "testuser"}' \
http://localhost:5000/list_posts

curl -X PATCH -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "id": 3, "title": "korchma"}' \
http://localhost:5000/update_post

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "title": "private", "description": "private", "is_private": true}' \
http://localhost:5000/create_post

curl -X GET -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassS1", "page_number": 0, "page_size": 10, "author": "testuser"}' \
http://localhost:5000/list_posts

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser1", "password": "testpasS1", "email": "testemail@example.com"}' \
http://localhost:5000/register

curl -X GET -H "Content-Type: application/json" \
-d '{"username": "testuser1", "password": "testpasS1", "page_number": 0, "page_size": 10, "author": "testuser"}' \
http://localhost:5000/list_posts
