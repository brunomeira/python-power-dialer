# Python Power Dialer
This project was built on Python 3.6.2. For simplicity purposes, no other tool was used. However, architecture was designed having extensibility in mind. One can easily add different technologies for storage or for managing distributed locks without changing the core of the business logic.

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
