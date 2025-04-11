FROM python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY wait-for-it.sh /wait-for-it.sh

CMD ["./wait-for-it.sh", "db:5432", "--", "python", "main.py"]