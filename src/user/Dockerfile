FROM python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-it.sh /wait-for-it.sh
COPY start.sh /start.sh

RUN chmod +x ./wait-for-it.sh ./start.sh

CMD ["./start.sh"]