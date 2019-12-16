class MemoryStorageLead:
    def __init__(self):
        self.storage = {}

    def update_lead_in_progress(self, agent_id: str, phone_number: str):
        self.storage[agent_id+"-"+phone_number] = "in_progress"


