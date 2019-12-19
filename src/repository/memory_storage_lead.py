import uuid
import time
from contextlib import contextmanager
from ..business import PendingLeadCall, CompletedLeadCall, FailedLeadCall, StartedLeadCall

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

    def update_lead_started(self, agent_id: str, phone_number: str):
        self.storage[phone_number] = (agent_id, "started")
        return StartedLeadCall(agent_id, phone_number)

    def update_lead_fail(self, phone_number: str):
        record = self.find_lead(phone_number)
        self.storage[phone_number] = (record.agent_id, "failed")
        return FailedLeadCall(record.agent_id, phone_number)

    def update_lead_complete(self, phone_number: str):
        record = self.find_lead(phone_number)
        self.storage[phone_number] = (record.agent_id, "completed")
        return CompletedLeadCall(record.agent_id, phone_number)

    def find_leads_started_by_agent(self, agent_id: str):
        results = []
        for key, value in self.storage.items():
            if value[0] == agent_id:
                results.append(key)

        return results

    def find_lead(self, phone_number: str):
        result = self.storage.get(phone_number, None)
        if result == None: return None
        if result[1] == "started": return StartedLeadCall(result[0], phone_number)
        if result[1] == "completed": return CompletedLeadCall(result[0], phone_number)
        if result[1] == "failed": return FailedLeadCall(result[0], phone_number)

