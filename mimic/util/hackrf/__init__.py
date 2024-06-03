import subprocess
import time

def sweep(min_frequency: int, max_frequency: int, output_file: str = None, num_sweeps: int = None):

    arguments = ['hackrf_sweep', '-f', f'{min_frequency}:{max_frequency}']

    if num_sweeps:
        arguments.extend(['-N', str(num_sweeps)])
    
    if output_file is None:
        output_file = f'./data/tmp/{int(time.time())}.csv'

    arguments.extend(['-r', output_file])

    subprocess.run(arguments)

    return output_file

def receive(set_freq_hz: int, sample_rate_hz: int, output_file: str = None, num_samples: int = None):

    arguments = ['hackrf_transfer', '-f', str(set_freq_hz), '-s', str(sample_rate_hz)]

    if num_samples:
        arguments.extend(['-n', str(num_samples)])
    
    if output_file is None:
        output_file = f'./data/tmp/{set_freq_hz}_{sample_rate_hz}_{int(time.time())}.bin'

    arguments.extend(['-r', output_file])

    subprocess.run(arguments)

    return output_file

def transmit(center_freq_hz: int, sample_rate_hz: int, input_file: str):
    
    arguments = ['hackrf_transfer', '-f', str(center_freq_hz), '-s', str(sample_rate_hz), '-t', input_file]

    subprocess.run(arguments)

    return True

if __name__ == '__main__':
    out = sweep(2400, 2500, num_sweeps=10)