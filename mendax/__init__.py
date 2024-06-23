import enum
import os
import time
import logging
from types import SimpleNamespace

from mendax.util.hackrf.core import receive_to_file_for_time, transmit_from_file

logging.basicConfig(
    filename='./logs/mendax.log',
    level = logging.DEBUG,
    format = '[%(asctime)s] %(message)s',
    datefmt='%m-%d-%Y %H:%M:%S'
)

class MendaxState(enum.Enum):
    IDLE = 0
    SLEEPING = 1
    OBSERVING = 2
    THINKING = 3
    BROADCASTING = 4
    CRASH = 5
    RECOVER = 6
    DYING = 7
    DEAD = 8

class Mendax:

    def __init__(self, **kwargs):
        self.state = MendaxState.IDLE
        self.state_function_map = self._init_state_function_map()

        self.state_parameters = SimpleNamespace(**kwargs) if kwargs else SimpleNamespace()

        self._initialize_directories()

        # Default parameters
        self.should_live = True
        self.state_parameters.crash_buffer = ''
        self.state_parameters.future_state_queue = [] if not hasattr(self.state_parameters, 'future_state_queue') else self.state_parameters.future_state_queue
        self.state_parameters.broadcast_immediately = False if not hasattr(self.state_parameters, 'broadcast_immediately') else self.state_parameters.broadcast_immediately
        self.state_parameters.broadcast_forever = False if not hasattr(self.state_parameters, 'broadcast_forever') else self.state_parameters.broadcast_forever

        self.loop_interval = 0.5

    def _initialize_directories(self):
        if not os.path.exists('./data'):
            os.mkdir('./data')
        
        if not os.path.exists('./data/tmp'):
            os.mkdir('./data/tmp')

        if not os.path.exists('./logs'):
            os.mkdir('./logs')

    def run(self):
        while self.should_live:
            self._loop_cycle()
    
    def _loop_cycle(self):
        try:
            logging.debug(f'In state {self.state}')
            self.state_function_map[self.state]()
        except Exception as e:
            self.state_parameters.crash_buffer = str(e)
            self.state = MendaxState.CRASH
        
        time.sleep(0.5)

    def _init_state_function_map(self):
        return {
            MendaxState.IDLE: self._idle_state,
            MendaxState.SLEEPING: self._sleeping_state,
            MendaxState.OBSERVING: self._observing_state,
            MendaxState.THINKING: self._thinking_state,
            MendaxState.BROADCASTING: self._broadcasting_state,
            MendaxState.CRASH: self._crash_state,
            MendaxState.RECOVER: self._recover_state,
            MendaxState.DYING: self._dying_state,
            MendaxState.DEAD: self._dead_state
        }
    
    def _idle_state(self):
        # TODO handle state transitions
        logging.debug(f'Handling IDLE state')
        # logging.debug(f'Awaiting user input...')

        if self.state_parameters.future_state_queue:
            self.state = self.state_parameters.future_state_queue.pop(0)
        else:
            pass


        # MUST capture `center_freq_hz`, `sample_rate_hz`, and (optional) `duration_s`
        # and add to `self.state_parameters`

    def _sleeping_state(self):
        # TODO implement
        logging.debug(f'Handling SLEEPING state')
        logging.debug(f'Timing out...')

    def _observing_state(self):
        '''
            This is the state where the Mendax is listening to signals.
        '''
        logging.debug(f'Handling OBSERVING state')

        logging.debug(f'Initiating HackRF receive for 30s with following parameters:')
        logging.debug(f'Center Frequency: {self.state_parameters.center_freq_hz}')
        logging.debug(f'Sample Rate: {self.state_parameters.sample_rate_hz}')
        logging.debug(f'Duration: {self.state_parameters.duration_s}')

        output_file = receive_to_file_for_time(
            self.state_parameters.center_freq_hz,
            self.state_parameters.sample_rate_hz,
            duration_s=self.state_parameters.duration_s
        )

        logging.debug(f'File saved to {output_file}')

        self.state_parameters.last_observation_file = output_file

        logging.debug(f'Observation complete, transitioning to THINKING state...')

        self.state = MendaxState.THINKING

    def _thinking_state(self):
        '''
            In this state, Mendax processes signals that it has received.

            At this time, we will simply log that we are processing signals. TODO.
        '''
        logging.debug(f'Handling THINKING state')
        logging.debug(f'Processing signals...')

        if self.state_parameters.broadcast_immediately:
            logging.debug(f'Broadcasting immediately...')
            logging.debug(f'Transitioning to BROADCASTING state...')
            self.state = MendaxState.BROADCASTING
        else:
            logging.debug(f'Transitioning to IDLE state...')
            self.state = MendaxState.IDLE

    def _broadcasting_state(self):
        # TODO implement
        logging.debug(f'Handling BROADCASTING state')
        logging.debug(f'Sending signals...')

        logging.debug(f'Initiating HackRF transmit with following parameters:')
        logging.debug(f'Center Frequency: {self.state_parameters.center_freq_hz}')
        logging.debug(f'Sample Rate: {self.state_parameters.sample_rate_hz}')
        logging.debug(f'Input File: {self.state_parameters.last_observation_file}')

        transmit_from_file(
            self.state_parameters.center_freq_hz,
            self.state_parameters.sample_rate_hz,
            self.state_parameters.last_observation_file
        )

        if self.state_parameters.broadcast_forever:
            logging.debug(f'Looping...')
            self.state = MendaxState.BROADCASTING
        else:
            logging.debug(f'Broadcast complete, transitioning to IDLE state...')
            self.state = MendaxState.IDLE

    def _crash_state(self):
        # TODO implement
        logging.debug(f'Handling CRASH state')
        logging.debug(f'Crashed with error: {self.state_parameters.crash_buffer}')

        match self.state_parameters.crash_buffer:
            case 'timeout':
                logging.debug(f'Attempting to recover...')
                self.state = MendaxState.RECOVER
            case 'user interrupt':
                logging.debug(f'Preparing to die...')
                self.state = MendaxState.DYING
            case _:
                logging.debug(f'Unknown error, dying...')
                self.state = MendaxState.DYING

    def _recover_state(self):
        # TODO implement
        logging.debug(f'Handling RECOVER state')
        logging.debug(f'Recovering from crash...')

        logging.debug(f'Reinitializing things...')

        self.state = MendaxState.IDLE

    def _dying_state(self):
        # TODO implement
        logging.debug(f'Handling DYING state')
        logging.debug(f'Preparing to die...')

        logging.debug(f'Cleaning up...')

        self.state = MendaxState.DEAD

    def _dead_state(self):
        # TODO implement
        logging.debug(f'Handling DEAD state')
        logging.debug(f'Already dead...')

        self.should_live = False