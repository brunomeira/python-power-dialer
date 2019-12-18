import uuid
import time
from contextlib import contextmanager

class MemoryStorageLead:
    def __init__(self, lock_timeout: int = 3):
        self.lock_state = {}
        self.storage = {}
        self.lock_timeout = lock_timeout

    @contextmanager
    def lock(self, lock_name):
        lock_id = self.grant_lock(lock_name)

        yield lock_id

        if lock_id != None:
            self.release_lock(lock_name, lock_id)

    def grant_lock(self, lock_name: str):
        """
        We can use redis or another implementation to guarantee distributed locking property. This is only to represent what we are doing.
        Timeout is not being used for this implementation but adding here. Ideally we should have it so it prevents deadlocks
        """
        hold_lock_ttl = 10
        attempt_timeout = self.lock_timeout

        lock_process_id = str(uuid.uuid4())
        grant_lock_until = time.time() + hold_lock_ttl

        attempt_until = time.time() + attempt_timeout

        while time.time() < attempt_until:
            if lock_name not in self.lock_state:
                self.lock_state[lock_name] = (lock_process_id, grant_lock_until)
                return lock_process_id

            time.sleep(.001)

        return None

    def release_lock(self, lock_name:str, lock_id: str):
        lock_state = self.lock_state.get(lock_name, None)

        # Corner case to take care of case where timeout expired due thread taking too long and another thread took control over it. We should not release lock if lock_ids do not match
        if lock_name != None and lock_state[0] == lock_id:
            return self.lock_state.pop(lock_name) != None

        return True

    def update_lead_in_progress(self, agent_id: str, phone_number: str):
        self.storage[phone_number] = (agent_id, "in_progress")
        return self.storage[phone_number]

    def update_lead_fail(self, phone_number: str):
        record = self.find_lead(phone_number)
        self.storage[phone_number] = (record[0], "failed")
        return self.storage[phone_number]

    def update_lead_complete(self, phone_number: str):
        record = self.find_lead(phone_number)
        self.storage[phone_number] = (record[0], "complete")
        return self.storage[phone_number]

    def find_leads_in_progress_by_agent(self, agent_id: str):
        results = []
        for key, value in self.storage.items():
            if value[0] == agent_id:
                results.append(key)

        return results

    def find_lead(self, phone_number: str):
        return self.storage.get(phone_number, None)

