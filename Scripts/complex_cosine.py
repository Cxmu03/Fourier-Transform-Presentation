import numpy as np
import matplotlib.pyplot as plt

xs = np.linspace(0, 10, 5000)

ys = np.e ** ((-1j) * 2 * np.pi * 0.5 * xs)
reals = [c.real for c in ys]
imags = [c.imag for c in ys]

ax = plt.figure().add_subplot(projection="3d")
ax.set_proj_type("ortho")

ax.plot(xs, reals, imags)
ax.set_xlabel("t")
ax.set_ylabel("Re")
ax.set_zlabel("Im")
plt.show()
