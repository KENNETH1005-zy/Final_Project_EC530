import json
import time
from messaging import MessageBroker

def on_analysis_result(data):
    print("\n📋 [subscriber] Analysis Result Received:")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    broker = MessageBroker()
    broker.subscribe("analysis_result", on_analysis_result)
    print("🔔 Subscribed to 'analysis_result'. Waiting for messages…")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Subscriber exiting.")