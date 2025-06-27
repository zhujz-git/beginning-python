import numpy as np
import matplotlib.pyplot as plt


def f1(t):
    return np.arcsin(np.sin(t) )


def f2(t):
    return np.sin(t) + 1.0/3.0*np.sin(3*t) + 1.0/5.0*np.sin(5*t) + 1.0/10*np.sin(10*t)


def f3(t):
    return np.sin(np.pi*2*t)


a = np.arange(-10.0, 10.0, 0.01)
plt.subplot(321)
plt.plot(a, f1(a))
plt.axis([-10, 10, -2, 2])
plt.grid(True)

plt.subplot(322)
b = np.arange(0.0, 33.0, 1)
plt.plot(b, [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8,
         8, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, ])
plt.axis([0, 33, 0, 9])
plt.grid(True)

plt.subplot(323)
x = np.arange(0, 25, 1)
b = np.full(25, 40)
b = b * [0, 1.0/12, 3.0/12, 6.0/12, 9.0/12, 11.0/12, 12.0/12,
         11.0/12, 9.0/12, 6.0/12, 3.0/12, 1.0/12, 0.0/12, 1.0 /
         12, 3.0/12, 6.0/12, 9.0/12, 11.0/12, 12.0/12,
         11.0/12, 9.0/12, 6.0/12, 3.0/12, 1.0/12, 0]
plt.plot(x, b)
plt.axis([0, 25, 0, 40])
plt.grid(True)

plt.subplot(324)
plt.plot(a, f2(a))
plt.axis([-10, 10, -2, 2])
plt.grid(True)
plt.show()

plt.subplot(325)
a = np.arange(-10.0, 10.0, 0.02)
plt.plot(a, f3(a))
plt.axis([-1, 3, -2, 2])
plt.grid(True)
plt.savefig('mat_test', dpi=1200)
plt.show()
