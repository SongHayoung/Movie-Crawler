import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

class KafkaService:
    def publish(self, movieName):
        producer = KafkaProducer(acks=1, bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send('movie',movieName)

    def consume(self,val=10):
        consumer = KafkaConsumer('movie', group_id='movie-consumer', bootstrap_servers='localhost:9092', enable_auto_commit=False, auto_offset_reset='earliest', value_deserializer=lambda v: json.loads(v.decode('utf-8')), consumer_timeout_ms=1000)
        rank = {}
        for message in consumer:
            if message.value in rank:
                rank[message.value] += 1
            else:
                rank[message.value] = 1

        return sorted(rank.items(), key=(lambda x:x[1]), reverse=True)[:val]
