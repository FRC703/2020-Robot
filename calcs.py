wheel_height = [5.5, 7, 6]
wall_height = [9.5, 7, 10]

import matplotlib.pyplot as plt
import numpy as np

plt.xkcd()
eq = np.polyfit(wheel_height, wall_height, 2)
xp = np.linspace(5, 8, 100)

p = np.poly1d(eq)


plt.title("Wall hit point based off wheel height")
plt.xlabel("Wheel Height")
plt.ylabel("Wall Height")
plt.scatter(wheel_height, wall_height, color="g", zorder=5)
plt.plot(xp, p(xp), "r-", zorder=2)

plt.show()
