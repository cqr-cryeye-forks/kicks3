FROM python:2.7-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --requirement requirements.txt

COPY . .
ENTRYPOINT ["python", "kicks3/kicks3.py"]
