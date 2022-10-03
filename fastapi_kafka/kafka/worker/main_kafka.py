import config
from redis import Redis
from aiokafka import AIOKafkaConsumer

redis_object = Redis(
    host=config.REDIS['host'], port=config.REDIS['port'],
    password=config.REDIS['pass'], db=config.REDIS['db']
)
