# Python Power Dialer
This project was built on Python 3.6.2. For simplicity purposes, no other tool was used. However, the architecture was designed having extensibility in mind. One can easily add different technologies for storage or for managing distributed locks without changing the core of the business logic.

## How to run
To run the project simply run

    python main.py


## Architecture
The project consists of 3 main layers:
 - Business
 - Repository
 - Services

### Business
The core of our project. It manages the flow of a lead based on events received from a desired queue system(Only restriction right now is that it must guarantee message ordering). It calls a lead when an agent logs in, ends a call when an agent logs out, and makes sure that a lead goes through correct flow of events.

### Repository
This layer is responsible for managing storage of business entities. For this project, it takes care of storing the state of a lead, the agent associated with it, and lastly it locks other distributed threads from executing an operation to a lead if another operation is in progress.

### Services
The service layer. Not much here, it just calls external services to dial a lead or get a new lead from pool. Implementation is TBD by business requirements.

## Tests
This project uses Python's default unittest framework.
To run tests simply run

    python -m unittest

## Call examples
Examples of how to instantiate a new power_dialer and execute calls

    from src.repository import MemoryStorageLead
    from src.business import PowerDialer
    lock_timeout = 2 # time in seconds
    repo = MemoryStorageLead(lock_timeout)  # This can be the remote data storage and lock manager
    
    agent_id = "1"
    power_dialer = PowerDialer(agent_id, repo)
    # Call proper power_dialer events ...
