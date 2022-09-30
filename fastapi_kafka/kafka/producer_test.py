from aiokafka import AIOKafkaProducer
import asyncio

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        for i in [1, 2, 3, 4, 5]:
            await producer.send_and_wait("my_topic", "Super message_{}".format(i).encode('utf-8'))
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

asyncio.run(send_one())


# from confluent_kafka import Producer
#
# p = Producer({'bootstrap.servers': 'localhost:9092'})
#
#
# def delivery_report(err, msg):
#     """ Called once for each message produced to indicate delivery result.
#         Triggered by poll() or flush(). """
#     if err is not None:
#         print('Message delivery failed: {}'.format(err))
#     else:
#         print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
#
#
# some_data_source = [str(i) for i in range(100)]
#
#
# for data in some_data_source:
#     # Trigger any available delivery report callbacks from previous produce() calls
#     p.poll(0)
#
#     # Asynchronously produce a message. The delivery report callback will
#     # be triggered from the call to poll() above, or flush() below, when the
#     # message has been successfully delivered or failed permanently.
#     p.produce('my_topic', data.encode('utf-8'), callback=delivery_report)
#
# # Wait for any outstanding messages to be delivered and delivery report
# # callbacks to be triggered.
# p.flush()