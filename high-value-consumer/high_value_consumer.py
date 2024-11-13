from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://mongodb:27017/')
db = client['fraud_detection']
collection = db['high_value_transactions']

# Kafka consumer setup
consumer = KafkaConsumer(
    'high_value_transactions',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='high_value_storage_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    collection.insert_one(transaction)
    print(f"Stored high-value transaction: {transaction}")
