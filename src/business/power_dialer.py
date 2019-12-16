from ..services import dial, get_lead_phone_number_to_dial

class PowerDialer:
    DIAL_RATIO = 2

    def __init__(self, agent_id: str, repository):
        self.agent_id     = agent_id
        self.repository   = repository

    def on_agent_login(self):
        for call_number in range(PowerDialer.DIAL_RATIO):
            phone_number = get_lead_phone_number_to_dial()

            if(phone_number != None and dial(self.agent_id, phone_number) == True):
                self.repository.update_lead_in_progress(self.agent_id, phone_number)

    def on_agent_logout(self):
        raise NotImplementedError

    def on_call_started(self, lead_phone_number: str):
        raise NotImplementedError

    def on_call_failed(self, lead_phone_number: str):
        raise NotImplementedError

    def on_call_ended(self, lead_phone_number: str):
        raise NotImplementedError
