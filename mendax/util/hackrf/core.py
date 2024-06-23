import subprocess
import time
import psutil

def sweep(min_frequency: int, max_frequency: int, output_file: str = None, num_sweeps: int = None):

    arguments = ['hackrf_sweep', '-f', f'{min_frequency}:{max_frequency}']

    if num_sweeps:
        arguments.extend(['-N', str(num_sweeps)])
    
    if output_file is None:
        output_file = f'./data/tmp/{int(time.time())}.csv'

    arguments.extend(['-r', output_file])

    subprocess.run(arguments)

    return output_file

def receive_to_file(center_freq_hz: int, sample_rate_hz: int, output_file: str = None, num_samples: int = None):

    arguments = ['hackrf_transfer', '-f', str(center_freq_hz), '-s', str(sample_rate_hz)]

    if num_samples:
        arguments.extend(['-n', str(num_samples)])
    
    if output_file is None:
        output_file = f'./data/tmp/{center_freq_hz}_{sample_rate_hz}_{int(time.time())}.bin'

    arguments.extend(['-r', output_file])

    subprocess.run(arguments)

    return output_file

def receive_to_file_for_time(center_freq_hz: int, sample_rate_hz: int, output_file: str = None, duration_s: int = None):
    '''
        This is a blocking function that will receive for a set duration of time.
    '''

    arguments = ['hackrf_transfer', '-f', str(center_freq_hz), '-s', str(sample_rate_hz)]
    
    if output_file is None:
        output_file = f'./data/tmp/{center_freq_hz}_{sample_rate_hz}_{int(time.time())}.bin'

    arguments.extend(['-r', output_file])

    receiving_subprocess = subprocess.Popen(arguments)

    subprocess_wrapper = psutil.Process(receiving_subprocess.pid)

    try:
        subprocess_wrapper.wait(timeout = duration_s)
    except psutil.TimeoutExpired:
        subprocess_wrapper.kill()

    return output_file

def transmit_from_file(center_freq_hz: int, sample_rate_hz: int, input_file: str):
    
    arguments = ['hackrf_transfer', '-f', str(center_freq_hz), '-s', str(sample_rate_hz), '-t', input_file]

    subprocess.run(arguments)

    return True

if __name__ == '__main__':
    out = receive_to_file_for_time(433920000, 2000000, duration_s=5)