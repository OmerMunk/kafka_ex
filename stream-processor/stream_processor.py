from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka consumer and producer setup
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='fraud_detection_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for message in consumer:
    transaction = message.value
    if transaction['potential_fraud']:
        producer.send('fraud_alerts', value=transaction)
        print(f"Fraudulent transaction detected: {transaction}")
    elif transaction['amount'] > 3000.0:
        producer.send('high_value_transactions', value=transaction)
        print(f"High-value transaction detected: {transaction}")
    else:
        # Write normal transactions to a CSV file
        with open('/app/normal_transactions.csv', 'a') as f:
            f.write(f"{transaction['transaction_id']},{transaction['user_id']},{transaction['amount']},{transaction['timestamp']}\n")
        print(f"Normal transaction logged: {transaction}")
