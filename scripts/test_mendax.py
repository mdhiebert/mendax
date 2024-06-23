from mendax import Mendax, MendaxState

future_state_queue = [
    MendaxState.OBSERVING,
]

center_freq_hz = 2.7085e7
sample_rate_hz = 0.006e7
duration_s = 5

mendax = Mendax(
    center_freq_hz = center_freq_hz,
    sample_rate_hz = sample_rate_hz,
    duration_s = duration_s,
    broadcast_immediately = True,
    brodacast_forever = False,
    future_state_queue = future_state_queue
)

mendax.run()