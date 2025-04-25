import time
from messaging import MessageBroker

broker = MessageBroker()
print("⏳ Monitoring Redis channels. Press Ctrl+C to stop.")
try:
    while True:
        topics = broker.list_topics()
        subs   = broker.list_listeners("analysis_result")
        print(f"Channels: {topics} | Subscribers on 'analysis_result': {subs}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n👋 Monitor stopped.")