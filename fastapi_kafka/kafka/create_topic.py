from confluent_kafka.admin import AdminClient, NewTopic


admin_client = AdminClient({
    "bootstrap.servers": "localhost:9092"
})

topic_list = []
topic_list.append(NewTopic("requests", 4, 1))
admin_client.create_topics(topic_list)