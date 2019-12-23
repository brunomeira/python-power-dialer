import uuid
import time
from contextlib import contextmanager
from ..business import PendingLeadCall, CompletedLeadCall, FailedLeadCall, StartedLeadCall,CalledLeadCall
from ..business import OnlineAgent, OfflineAgent

class MemoryStorageLead:
    def __init__(self, lock_timeout: int = .5):
        self.lock_state = {}
        self.storage = {}
        self.log = []
        self.agent_storage = {}
        self.lock_timeout = lock_timeout

    @contextmanager
    def lock(self, lock_name):
        try:
            lock_id = self.grant_lock(lock_name)
            if(lock_id is None): raise Exception("Lock not acquired")

            yield lock_id
        finally:
            if lock_id is not None: self.release_lock(lock_name, lock_id)

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

            time.sleep(.01)

        return None

    def release_lock(self, lock_name:str, lock_id: str):
        lock_state = self.lock_state.get(lock_name, None)

        # Corner case to take care of case where timeout expired due thread taking too long and another thread took control over it. We should not release lock if lock_ids do not match
        if lock_name is not None and lock_state[0] == lock_id:
            return self.lock_state.pop(lock_name) is not None

        return True

    def update_lead_started(self, agent_id: str, phone_number: str):
        self.storage[phone_number] = (agent_id, "started")
        return StartedLeadCall(agent_id, phone_number, self)

    def update_lead_fail(self, phone_number: str):
        record = self.find_lead(phone_number)
        self.storage[phone_number] = (record.agent_id, "failed")
        return FailedLeadCall(record.agent_id, phone_number, self)

    def update_lead_called(self, agent_id: str, phone_number: str):
        self.storage[phone_number] = (agent_id, "called")
        return CalledLeadCall(agent_id, phone_number, self)

    def update_lead_complete(self, phone_number: str):
        record = self.find_lead(phone_number)
        self.storage[phone_number] = (record.agent_id, "completed")
        return CompletedLeadCall(record.agent_id, phone_number, self)

    def update_agent_online(self, agent_id):
        self.agent_storage[agent_id] = (agent_id, "online")
        return OnlineAgent(agent_id, self)

    def update_agent_offline(self, agent_id):
        self.agent_storage[agent_id] = (agent_id, "offline")
        return OfflineAgent(agent_id, self)

    def find_leads_started_by_agent(self, agent_id: str):
        results = []
        for key, value in self.storage.items():
            if value[0] == agent_id and value[1] == "started":
                results.append(key)

        return results

    def find_lead(self, phone_number: str):
        result = self.storage.get(phone_number, None)
        if result is None: return PendingLeadCall(None, phone_number, self)
        if result[1] == "called": return CalledLeadCall(result[0], phone_number, self)
        if result[1] == "started": return StartedLeadCall(result[0], phone_number, self)
        if result[1] == "completed": return CompletedLeadCall(result[0], phone_number, self)
        if result[1] == "failed": return FailedLeadCall(result[0], phone_number, self)

    def find_agent(self, agent_id):
        result = self.agent_storage.get(agent_id, None)
        if result is None: return OfflineAgent(agent_id, self)
        if result[1] == "online": return OnlineAgent(result[0], self)
        if result[1] == "offline": return OfflineAgent(result[0], self)

    def add_log(self, log):
        self.log.append(log)
