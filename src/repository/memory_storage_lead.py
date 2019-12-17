class MemoryStorageLead:
    def __init__(self):
        self.storage = {}

    def update_lead_pending(self, phone_number: str):
        self.storage[phone_number] = (None, "pending")
        return self.storage[phone_number]

    def update_lead_in_progress(self, agent_id: str, phone_number: str):
        self.storage[phone_number] = (agent_id, "in_progress")
        return self.storage[phone_number]

    def update_lead_fail(self, phone_number: str):
        record = self.storage[phone_number]
        self.storage[phone_number] = (record[0], "failed")
        return self.storage[phone_number]

    def update_lead_complete(self, phone_number: str):
        record = self.storage[phone_number]
        self.storage[phone_number] = (record[0], "complete")
        return self.storage[phone_number]

