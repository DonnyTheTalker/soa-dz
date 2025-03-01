cd src && docker-compose up --build

curl -X GET "http://localhost:5000/user?username=testuser"

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass", "email": "testemail@example.com"}' \
http://localhost:8000/register

curl -X PATCH -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass", "phone_number": "8800553535"}' \
http://localhost:8000/update_profile

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}' \
http://localhost:8000/post