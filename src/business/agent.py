from abc import ABC

class Agent(ABC):
    """
    Base class to represent an agent state.
    Current state transitions are:
    inactive -> active
    active -> inactive
    """
    def __init__(self, agent_id, repository):
        self.agent_id = agent_id
        self.repository = repository

    def transition_to(self, state):
        pass

    def __str__(self):
        return "{}(agent_id: {}, state: {})".format(self.__class__.__name__, self.agent_id, self.state)

    def __eq__(self, other):
        return self.state == other.state and self.agent_id == other.agent_id


class OnlineAgent(Agent):
    def __init__(self, agent_id, repository):
        super().__init__(agent_id, repository)
        self.state = "online"

    def transition_to(self, state):
        if state == self.state: return self
        if state == "offline":
            self.repository.update_agent_offline(self.agent_id)
            return OfflineAgent(self.agent_id, self.repository)

        raise Exception("{}: Transition from {} to {} is invalid".format(self, self.state, state))

class OfflineAgent(Agent):
    def __init__(self, agent_id, repository):
        super().__init__(agent_id, repository)
        self.state = "offline"

    def transition_to(self, state):
        if state == self.state: return self
        if state == "online":
            self.repository.update_agent_online(self.agent_id)
            return OnlineAgent(self.agent_id, self.repository)

        raise Exception("{}: Transition from {} to {} is invalid".format(self, self.state, state))
