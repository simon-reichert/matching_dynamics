import networkx as nx
import matplotlib.pyplot as plt
from matching import Network, get_edgetrap
from matplotlib.animation import FuncAnimation
import time

N, pos = get_edgetrap(4)
fig, ax = plt.subplots(1,1)
N.draw(pos, ax=ax)

def start():
    N.draw(pos, ax=ax)

def update(frame):
    plt.cla()
    N.best_step(True)
    N.draw(pos, ax=ax)

ani = FuncAnimation(fig, update, 10, interval=4000, init_func=start)

plt.show()