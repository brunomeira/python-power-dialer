from concurrent.futures import wait, ALL_COMPLETED, ThreadPoolExecutor
import threading
from src.business import PowerDialer
from src.repository import MemoryStorageLead
import uuid
import random
import csv

lock_timeout = 3
repository = MemoryStorageLead(lock_timeout)

def push_event(event, agent_id, lead_phone_number):
    power_dialer = PowerDialer(agent_id, repository)
    if event == "login": power_dialer.on_agent_login()
    if event == "logout": power_dialer.on_agent_logout()
    if event == "started": power_dialer.on_call_started(lead_phone_number)
    if event == "ended": power_dialer.on_call_ended(lead_phone_number)
    if event == "failed": power_dialer.on_call_failed(lead_phone_number)

def generate_events():
    """
    This is a mock of events being received by our queue system
    """
    events = []
    with open('events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
           events.append(tuple(row))

    return events

pool = ThreadPoolExecutor(max_workers=5)
futures = [pool.submit(push_event, *event) for event in generate_events()]

wait(futures, return_when = ALL_COMPLETED)
print(repository.storage)




