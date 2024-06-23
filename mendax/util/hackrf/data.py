import datetime

# SWEEP

class SweepDatum:

    def __init__(self, date_str: str, time_str: str, hz_low: int, hz_high: int, hz_bin_width: int, num_samples: int, *bins: int):
        self.timestamp = datetime.datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M:%S.%f')

        self.hz_low = int(hz_low)
        self.hz_high = int(hz_high)
        self.hz_bin_width = int(hz_bin_width)
        self.num_samples = int(num_samples)

        self._samples = [int(bin) for bin in bins]
        self._sample_freqs = [hz_low + (i * hz_bin_width) for i in range(len(bins))]

    def __iter__(self):
        for (freq, sample) in zip(self._sample_freqs, self._samples):
            yield (freq, sample)


class SweepData:

    def __init__(self, sweep_data: list[SweepDatum]):

        self._data = {}

        for datum in sweep_data:
            if not isinstance(datum, SweepDatum):
                raise ValueError('SweepData must be initialized with a list of SweepDatum objects')
            
            if datum.timestamp not in self._data:
                self._data[datum.timestamp] = []

            for (freq, sample) in datum:
                self._data[datum.timestamp].append((freq, sample))
            
        for timestamp in self._data:
            self._data[timestamp] = sorted(self._data[timestamp], key = lambda datum: datum[0])

        # TODO

# TX/RX