from kafka import KafkaConsumer
import json

# Kafka consumer setup
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='transaction_logger_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    if not transaction['potential_fraud'] and transaction['amount'] <= 3000.0:
        with open('/app/normal_transactions.csv', 'a') as f:
            f.write(f"{transaction['transaction_id']},{transaction['user_id']},{transaction['amount']},{transaction['timestamp']}\n")
        print(f"Logged normal transaction: {transaction}")
