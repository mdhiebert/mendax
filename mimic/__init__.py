import enum
import time
import logging

class State(enum.Enum):
    IDLE = 0
    SLEEPING = 1
    OBSERVING = 2
    THINKING = 3
    BROADCASTING = 4
    CRASH = 5
    RECOVER = 6
    DYING = 7
    DEAD = 8

class Mimic:

    def __init__(self, id):

        
        self.state = State.IDLE
        self.state_function_map = self._init_state_function_map()

        self.should_live = True
        self.crash_buffer = ''

        self.loop_interval = 0.5

    def run(self):
        while self.should_live:
            self._loop_cycle()
    
    def _loop_cycle(self):
        try:
            logging.debug(f'In state {self.state}')
            self.state_function_map[self.state]()
        except Exception as e:
            self.crash_buffer = str(e)
            self.state = State.CRASH
        
        time.sleep(0.5)

    def _init_state_function_map(self):
        return {
            State.IDLE: self._idle_state,
            State.SLEEPING: self._sleeping_state,
            State.OBSERVING: self._reading_state,
            State.THINKING: self._thinking_state,
            State.BROADCASTING: self._replying_state,
            State.CRASH: self._crash_state,
            State.RECOVER: self._recover_state,
            State.DYING: self._dying_state,
            State.DEAD: self._dead_state
        }
    
    def _idle_state(self):
        # TODO handle state transitions
        logging.debug(f'Handling IDLE state')
        logging.debug(f'Awaiting user input...')

    def _sleeping_state(self):
        # TODO implement
        logging.debug(f'Handling SLEEPING state')
        logging.debug(f'Timing out...')

    def _observing_state(self):
        # TODO implement
        logging.debug(f'Handling OBSERVING state')
        logging.debug(f'Listening to signals...')

    def _thinking_state(self):
        # TODO implement
        logging.debug(f'Handling THINKING state')
        logging.debug(f'Processing signals...')

    def _broadcasting_state(self):
        # TODO implement
        logging.debug(f'Handling BROADCASTING state')
        logging.debug(f'Sending signals...')

    def _crash_state(self):
        # TODO implement
        logging.debug(f'Handling CRASH state')
        logging.debug(f'Crashed with error: {self.crash_buffer}')

        match self.crash_buffer:
            case 'timeout':
                logging.debug(f'Attempting to recover...')
                self.state = State.RECOVER
            case 'user interrupt':
                logging.debug(f'Preparing to die...')
                self.state = State.DYING
            case _:
                logging.debug(f'Unknown error, dying...')
                self.state = State.DYING

    def _recover_state(self):
        # TODO implement
        logging.debug(f'Handling RECOVER state')
        logging.debug(f'Recovering from crash...')

        logging.debug(f'Reinitializing things...')

        self.state = State.IDLE

    def _dying_state(self):
        # TODO implement
        logging.debug(f'Handling DYING state')
        logging.debug(f'Preparing to die...')

        logging.debug(f'Cleaning up...')

        self.state = State.DEAD

    def _dead_state(self):
        # TODO implement
        logging.debug(f'Handling DEAD state')
        logging.debug(f'Already dead...')

        self.should_live = False