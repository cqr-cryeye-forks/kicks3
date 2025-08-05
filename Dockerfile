FROM python:3.13-slim
WORKDIR /app

COPY NEW/requirements.txt .
RUN pip install --requirement requirements.txt

COPY . .
ENTRYPOINT ["python3", "main.py"]
CMD ["--url", "example.com"]