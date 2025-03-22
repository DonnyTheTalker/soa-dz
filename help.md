cd src && docker compose up --build

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