import numpy as np
import matplotlib.pyplot as plt

# Generate sample I/Q data
I = np.cos(np.linspace(0, 2*np.pi, 1000))  # Cosine wave for I
Q = np.sin(np.linspace(0, 2*np.pi, 1000))  # Sine wave for Q

# Plot the I/Q data
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(I, label='In-Phase (I)')
plt.plot(Q, label='Quadrature (Q)')
plt.legend()
plt.title('I and Q Components')

plt.subplot(2, 1, 2)
plt.plot(I, Q, label='I vs Q')
plt.xlabel('In-Phase (I)')
plt.ylabel('Quadrature (Q)')
plt.legend()
plt.title('Constellation Diagram')

plt.tight_layout()
plt.show()
