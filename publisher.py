from google.cloud import pubsub_v1

# TODO(developer)
project_id = "iconic-access-309902"
topic_id = "mytopic"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
#projects/iconic-access-309902/topics/mytopic
topic_path = publisher.topic_path(project_id, topic_id)

for n in range(1, 10):
    data = "Message number {}".format(n)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

print("Published messages to {topic_path}.")
