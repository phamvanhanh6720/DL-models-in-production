import config
from redis import Redis
from aiokafka import AIOKafkaProducer

redis_object = Redis(
    host=config.REDIS['host'], port=config.REDIS['port'],
    password=config.REDIS['pass'], db=config.REDIS['db']
)


producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_CONNECTION)