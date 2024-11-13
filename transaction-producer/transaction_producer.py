from kafka import KafkaProducer
import json
import time
import random
import uuid

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

users = [str(uuid.uuid4()) for _ in range(100)]  # Simulate 100 users

blacklisted_users = users[:5]  # First 5 users are blacklisted

while True:
    transaction = {
        'transaction_id': str(uuid.uuid4()),
        'user_id': random.choice(users),
        'amount': round(random.uniform(0.01, 10000.0), 2),
        'timestamp': time.time()
    }

    if (transaction['amount'] > 5000.0) or (transaction['amount'] < 0.02) or (transaction['user_id'] in blacklisted_users):
        transaction['potential_fraud'] = True
    else:
        transaction['potential_fraud'] = False

    producer.send('transactions', value=transaction)
    print(f"Produced transaction: {transaction}")
    time.sleep(random.uniform(0.1, 1.0))
