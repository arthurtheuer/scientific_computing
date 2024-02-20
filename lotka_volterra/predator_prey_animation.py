import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def f(x, a, b, g, d):  # returns function value of Lokta-Volterra system
    return np.array([[a*x[0, 0]-b*x[0, 0]*x[1, 0]], [d*x[0, 0]*x[1, 0]-g*x[1, 0]]])


def J(x, a, b, g, d):  # Jacobian function
    return np.array([[a-b*x[1, 0], -b*x[0, 0]], [d*x[1, 0], d*x[0, 0]-g]])


def forward_euler(x, h, N, a, b, g, d):
    result = np.zeros((x.shape[0], N+1))  # pre-allocate result array
    result[:, 0] = x[:, 0]  # store the initial state in the result array

    for i in range(N):
        x_new = x + h * f(x, a, b, g, d)
        result[:, i+1] = x_new[:, 0]  # store the new state in the result array
        x = x_new

    return result


def runge_kutta_2(x, h, N, a, b, g, d):
    result = np.zeros((x.shape[0], N+1))  # pre-allocate result array
    result[:, 0] = x[:, 0]  # store the initial state in the result array

    for i in range(N):
        k1 = f(x, a, b, g, d)
        x_half = x + h/2 * k1  # go half a step and get new f
        k2 = f(x_half, a, b, g, d)

        x_new = x + h * k2  # go full step with f from midpoint
        result[:, i+1] = x_new[:, 0]  # store the new state in the result array
        x = x_new

    return result


def heun_method(x, h, N, a, b, g, d):
    result = np.zeros((x.shape[0], N+1))  # pre-allocate result array
    result[:, 0] = x[:, 0]  # store the initial state in the result array

    for i in range(N):
        k1 = f(x, a, b, g, d)
        x_tmp = x + h * k1  # calculate f at new step
        k2 = f(x_tmp, a, b, g, d)

        x_new = x + h/2 * (k1 + k2)  # average f at old and new step
        result[:, i+1] = x_new[:, 0]  # store the new state in the result array
        x = x_new

    return result


def runge_kutta_4(x, h, N, a, b, g, d):
    result = np.zeros((x.shape[0], N+1))  # pre-allocate result array
    result[:, 0] = x[:, 0]  # store the initial state in the result array

    for i in range(N):
        k1 = f(x, a, b, g, d)
        k2 = f(x + k1 * h/2, a, b, g, d)
        k3 = f(x + k2 * h/2, a, b, g, d)
        k4 = f(x + k3 * h, a, b, g, d)

        x_new = x + h/6 * (k1 + 2*k2 + 2*k3 + k4)
        result[:, i+1] = x_new[:, 0]  # store the new state in the result array
        x = x_new

    return result


def backward_euler(x, h, N, a, b, g, d, tolx):
    result = np.zeros((x.shape[0], N+1))  # pre-allocate result array
    result[:, 0] = x[:, 0]  # store the initial state in the result array

    I = np.eye(2)  # identity matrix
    x_new = x.copy()  # use initial x as a guess for x_new

    for i in range(N):
        x = x_new.copy()  # save x_new from previous step as "old" x

        while True:
            dx = np.linalg.solve(h * J(x_new, a, b, g, d) - I, x_new - x - h * f(x_new, a, b, g, d))
            x_new = x_new + dx  # update x_new with calculated difference

            if np.linalg.norm(dx) < tolx:  # check for convergence
                break

        result[:, i+1] = x_new[:, 0]  # save converged x_new for current step

    return result


alpha = 100  # rabbit reproduction rate
beta = 1.5  # fox kill rate
gamma = 10  # fox death rate
delta = 0.01  # relative fox reproduction rate

T = 1  # total simulation time
h = 0.002  # step size
N = int(np.ceil(T/h))  # number of time steps

tolx = 10**-10  # error tolerance for Newton's method in backward_euler

x = np.array([[1000], [100]])  # initial rabbit and fox population
t = h * np.arange(N+1)  # vector of time steps

y_fe = forward_euler(x, h, N, alpha, beta, gamma, delta)
y_mp = runge_kutta_2(x, h, N, alpha, beta, gamma, delta)
y_he = heun_method(x, h, N, alpha, beta, gamma, delta)
y_rk = runge_kutta_4(x, h, N, alpha, beta, gamma, delta)
y_be = backward_euler(x, h, N, alpha, beta, gamma, delta, tolx)


# ANIMATED PLOT

# Create a figure and subplots:
fig = plt.figure(figsize=(12, 6), dpi=100)

ax1 = fig.add_subplot(2, 2, 1)
ax1.set_title("Rabbit population numbers over time")
ax1.set_xlim(0, 1)
ax1.set_ylim((-392.57185824234375, 8353.347483234807))
ax1.set_xlabel(r"Time (T)")
ax1.set_ylabel("Population number (R)")

ax2 = fig.add_subplot(2, 2, 3)
ax2.set_title("Fox population numbers over time")
ax2.set_xlim(0, 1)
ax2.set_ylim((15.293604207936784, 171.1282678820827))
ax2.set_xlabel("Time (T)")
ax2.set_ylabel("Population number (F)")

ax3 = fig.add_subplot(1, 2, 2)
ax3.set_title("Fox and rabbit population equilibria")
ax3.set_xlim(-392.57185824234375, 8353.347483234807)
ax3.set_ylim((15.293604207936784, 171.1282678820827))
ax3.set_xlabel("Number of rabbits (R)")
ax3.set_ylabel("Number of foxes (F)")

# Create line objects for each plot:
line_fe_ax1, = ax1.plot([], [], label="Forward Euler", color="C0")
line_be_ax1, = ax1.plot([], [], label="Backward Euler", color="C2")
line_rk_ax1, = ax1.plot([], [], label="Runge-Kutta 4", color="C1")

line_fe_ax2, = ax2.plot([], [], label="Forward Euler", color="C0")
line_be_ax2, = ax2.plot([], [], label="Backward Euler", color="C2")
line_rk_ax2, = ax2.plot([], [], label="Runge-Kutta 4", color="C1")

line_fe_ax3, = ax3.plot([], [], label="Forward Euler", color="C0")
line_be_ax3, = ax3.plot([], [], label="Backward Euler", color="C2")
line_rk_ax3, = ax3.plot([], [], label="Runge-Kutta 4", color="C1")

ax1.legend(loc="upper left")
ax2.legend(loc="upper left")
ax3.legend(loc="upper right")


# Function that updates the lines for each animation frame:
def update(frame):
    line_fe_ax1.set_data(t[:frame], y_fe[0, :frame])
    line_rk_ax1.set_data(t[:frame], y_rk[0, :frame])
    line_be_ax1.set_data(t[:frame], y_be[0, :frame])

    line_fe_ax2.set_data(t[:frame], y_fe[1, :frame])
    line_rk_ax2.set_data(t[:frame], y_rk[1, :frame])
    line_be_ax2.set_data(t[:frame], y_be[1, :frame])

    line_fe_ax3.set_data(y_fe[0, :frame], y_fe[1, :frame])
    line_rk_ax3.set_data(y_rk[0, :frame], y_rk[1, :frame])
    line_be_ax3.set_data(y_be[0, :frame], y_be[1, :frame])


plt.tight_layout()

# Create and save the animation as a GIF:
ani = FuncAnimation(fig, update, frames=len(t), interval=10, repeat=False)

# ani.save("lotka_volterra/output/population_numbers.gif", fps=30)
# plt.show()
