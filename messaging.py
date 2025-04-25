import redis, json
from typing import Callable

class MessageBroker:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.redis = redis.Redis(host=host, port=port)
        self.pubsub = self.redis.pubsub()

    def publish(self, topic: str, message: dict):
        """Publish a Python dict as JSON on `topic`."""
        self.redis.publish(topic, json.dumps(message))

    def subscribe(self, topic: str, callback: Callable[[dict], None]):
        """
        Subscribe to JSON messages on `topic`.
        `callback` will be called with the decoded dict.
        """
        def _handler(msg):
            if msg["type"] == "message":
                callback(json.loads(msg["data"]))
        self.pubsub.subscribe(**{topic: _handler})
        self.pubsub.run_in_thread(sleep_time=0.001)

    def list_topics(self):
        """List all currently active channels."""
        return self.redis.execute_command("PUBSUB CHANNELS")

    def list_listeners(self, topic: str):
        """Return subscriber count for a given topic."""
        return self.redis.execute_command("PUBSUB NUMSUB", topic)