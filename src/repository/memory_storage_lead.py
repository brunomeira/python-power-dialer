class MemoryStorageLead:
    def __init__(self):
        self.storage = {}

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
        return self.storage[phone_number]

