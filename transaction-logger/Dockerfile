FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY transaction_logger.py .
CMD ["python", "transaction_logger.py"]
