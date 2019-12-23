from threading import Thread
import sys, traceback
from src.business import PowerDialer
from src.repository import MemoryStorageLead
import csv
import time
from queue import Queue

queue = Queue()
repository = MemoryStorageLead()

def push_event(queue):
    while True:
        event,agent_id,lead_phone_number = queue.get()
        queue.task_done()

        max_retry_attempts = 3
        retry_attempt = 0
        power_dialer = PowerDialer(agent_id, repository)

        while retry_attempt < max_retry_attempts:
            try:
                if event == "login": power_dialer.on_agent_login()
                if event == "logout": power_dialer.on_agent_logout()
                if event == "started": power_dialer.on_call_started(lead_phone_number)
                if event == "ended": power_dialer.on_call_ended(lead_phone_number)
                if event == "failed": power_dialer.on_call_failed(lead_phone_number)

                time.sleep(0.1) # Not needed, just to verify other threads work(test remote data store IO)
                break
            except Exception as a:
                time.sleep(0.1)
                retry_attempt+=1

def generate_events():
    """
    This is a mock of events being received by our queue system
    """
    with open('events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
           queue.put(tuple(row))

    return queue

events = generate_events()
total_threads = 10
for x in range(total_threads):
    worker = Thread(target=push_event, name=f"thread-{x}", args=(events,))
    worker.setDaemon(True)
    worker.start()

events.join()

print("Log calls")
[print(log) for log in repository.log]
print("----------------------")
print("Final Database state")
print(repository.storage)

