from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://mongodb:27017/')
db = client['fraud_detection']
collection = db['fraud_transactions']

# Kafka consumer setup
consumer = KafkaConsumer(
    'fraud_alerts',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='fraud_storage_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value

    collection.insert_one(transaction)
    # insert with a ttl of 1 minute
    # collection.insert_one(transaction, {'expireAfterSeconds': 60})

    print(f"Stored fraudulent transaction: {transaction}")
