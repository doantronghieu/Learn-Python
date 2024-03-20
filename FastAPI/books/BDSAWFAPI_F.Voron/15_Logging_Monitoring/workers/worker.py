import add_packages
import random
import time
import prometheus_client
import dramatiq
from dramatiq.brokers.redis import RedisBroker

#*=============================================================================
broker_redis = RedisBroker(host="localhost")
dramatiq.set_broker(broker=broker_redis)

#*=============================================================================
@dramatiq.actor()
def task_addition(a: int, b: int):
  time.sleep(1)
  print(a + b)

#*-----------------------------------------------------------------------------
DICE_COUNTER = prometheus_client.Counter(
  # uniquely identify the metric in Prometheus
  # metric names: [domain: http_|app_]ABC[unit: _seconds|_bytes|_total]
  name="app_dice_rolls_total",
  documentation="Total number of dice rolls labelled per face",
  # Set this label to the corresponding result face for each dice roll.
  labelnames=["face"],
)

@dramatiq.actor()
def task_roll_dice() -> int:
  result = random.randint(1, 6)
  time.sleep(1)
  DICE_COUNTER.labels(result).inc() # Increase the counter of `labelnames`
  return result

#*-----------------------------------------------------------------------------
if __name__ == "__main__":
  task_addition.send(3, 2)