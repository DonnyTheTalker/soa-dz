FROM python:3.11

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

COPY . .

CMD ["pytest"]