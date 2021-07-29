from google.cloud import pubsub_v1
import subprocess

PROJECT = "iconic-access-309902"
SUBSCRIPTION = "mytopic-sub"

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(PROJECT, SUBSCRIPTION)

response = subscriber.pull(
    request={
        "subscription": subscription_path,
        "max_messages": 1,
    }
)

TWITCH_VIDEO_ID = ""

#Read a single message from queue 
for msg in response.received_messages:
    print("Received twitch stream id for processing : ", msg.message.data)
    TWITCH_VIDEO_ID = msg.message.data
 
#Send ack for the message so that it gets deleted
ack_ids = [msg.ack_id for msg in response.received_messages]
subscriber.acknowledge(
    request={
        "subscription": subscription_path,
        "ack_ids": ack_ids,
    }
)



