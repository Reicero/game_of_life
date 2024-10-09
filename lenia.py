import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Définition des paramètres
size = 100
dx = 0.1
diff_rate = 0.01
feed_rate = 0.01
kill_rate = 0.01
dA = 0.05
dB = 0.025

# Initialisation des grilles A et B
A = np.ones((size, size)) * 0.5
B = np.zeros((size, size))

# Simulation de l'évolution de Lenia
def step():
    global A, B
    A_next = A + (diff_rate * (np.roll(A, 1, axis=0) + np.roll(A, -1, axis=0) +
                               np.roll(A, 1, axis=1) + np.roll(A, -1, axis=1) - 4 * A) / dx**2) - (A * B * B) + (feed_rate * (1 - A))
    B_next = B + (dA * (np.roll(B, 1, axis=0) + np.roll(B, -1, axis=0) +
                        np.roll(B, 1, axis=1) + np.roll(B, -1, axis=1) - 4 * B) / dx**2) + (A * B * B) - ((kill_rate + feed_rate) * B)
    A[:] = np.clip(A_next, 0, 1)
    B[:] = np.clip(B_next, 0, 1)

# Création de l'animation
fig, ax = plt.subplots()
im = ax.imshow(A, cmap='binary')

def update(frame):
    step()
    im.set_data(A)
    return im,

ani = animation.FuncAnimation(fig, update, frames=range(100), interval=50, blit=True)

plt.show()