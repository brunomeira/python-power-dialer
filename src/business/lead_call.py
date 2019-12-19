from abc import ABC

class LeadCall(ABC):
    """
    Base class to represent a lead by agent and state.
    Current state transitions are:
    pending -> start -> complete
    pending -> start -> fail
    """
    def __init__(self, agent_id, phone_number):
        self.agent_id = agent_id
        self.phone_number = phone_number

    def transition_to(self, state):
        pass

    def __str__(self):
        return "{}(agent_id: {}, phone_number: {}, state: {})".format(self.__class__.__name__, self.agent_id, self.phone_number, self.state)

    def __eq__(self, other):
        return self.state == other.state and self.agent_id == other.agent_id and self.phone_number == other.phone_number


class PendingLeadCall(LeadCall):
    def __init__(self, agent_id, phone_number):
        super().__init__(agent_id, phone_number)
        self.state = "pending"

    def transition_to(self, state):
        if state == self.state: return self
        if state == "started": return StartedLeadCall(self.agent_id, self.phone_number)

        raise Exception("Transition from {} to {} is invalid".format(self.state, state))


class StartedLeadCall(LeadCall):
    def __init__(self, agent_id, phone_number):
        super().__init__(agent_id, phone_number)
        self.state = "started"

    def transition_to(self, state):
        if state == self.state: return self

        if state == "completed": return CompletedLeadCall(self.agent_id, self.phone_number)
        if state == "failed": return FailedLeadCall(self.agent_id, self.phone_number)

        raise Exception("Transition from {} to {} is invalid".format(self.state, state))


class FailedLeadCall(LeadCall):
    def __init__(self, agent_id, phone_number):
        super().__init__(agent_id, phone_number)
        self.state = "failed"

    def transition_to(self, state):
        if state == self.state: return self
        raise Exception("Transition from {} to {} is invalid".format(self.state, state))

class CompletedLeadCall(LeadCall):
    def __init__(self, agent_id, phone_number):
        super().__init__(agent_id, phone_number)
        self.state = "completed"

    def transition_to(self, state):
        if state == self.state: return self
        raise Exception("Transition from {} to {} is invalid".format(self.state, state))
