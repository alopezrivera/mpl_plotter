import numpy as np
from scipy.interpolate import Rbf

from mpl_plotter.canvas import figure
from mpl_plotter.two_d import line, scatter, fill_area


"""
Composed fill plot example

Antonio Lopez Rivera, 2020
"""


"""
=============================================
=============================================
=============================================
Helpers
=============================================
=============================================
=============================================
"""


def rad(a):
    return a*np.pi/180


def deg(a):
    return a*180/np.pi


def target(value, n):
    return np.ones(n) * value


def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def derivative(f, dt):
    """
    Backwards difference derivation scheme
    """
    df = np.empty(f.size)

    for i in range(1, len(f)):
        df[i] = (f[i]-f[i-1])/dt
    """
    Filling first position of derivative vector
        Forwards difference derivation scheme
    """
    df[0] = (f[0]-f[1])/dt
    return df


def primitive(f, dt):
    f_prime = np.zeros(len(f))
    for i in range(1, len(f)):
        f_prime[i] = dt * (f[i] + (f[i-1] - f[i]) / 2)
    f_prime[0] = dt * (f[1] + (f[0] - f[1]) / 2)
    return f_prime


def create_cmap(r_start, g_start, b_start, r_end, g_end, b_end):
    from matplotlib.colors import ListedColormap

    N = 256

    red = np.ones((N, 4))
    red[:, 0] = np.linspace(r_start / N, r_end/N, N)
    red[:, 1] = np.linspace(g_start / N, g_end/N, N)
    red[:, 2] = np.linspace(b_start / N, b_end/N, N)

    return ListedColormap(red)


def combine_cmaps(cmap1, cmap2, cmap1_share=0.5):
    import matplotlib as mpl
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    lcmap1 = cm.get_cmap(cmap1) if not isinstance(cmap1, mpl.colors.Colormap) else cmap1
    lcmap2 = cm.get_cmap(cmap2) if not isinstance(cmap2, mpl.colors.Colormap) else cmap2
    result = np.vstack((lcmap1(np.linspace(0, 1, int(256*cmap1_share))),
                        lcmap2(np.linspace(1, 0, 256-int(256*cmap1_share)))))
    return ListedColormap(result, name='Combined')


def plot_signal(x, y,
                # Specifics
                color="darkred",
                line_width=1,
                # Labels
                x_label="", y_label="",
                # Legend
                plot_label=None,
                # Bounds
                x_bounds=None, y_bounds=None,
                # Ticks
                tick_number=None,
                # Other
                resize=True,
                zorder=None,
                ):
    from mpl_plotter.two_d import line
    y_label_rotation = 90 if len(y_label) > 3 else 0
    line(x=x, y=y,
         # Specifics
         line_width=line_width,
         color=color,
         # Title
         title="",
         # Ticks
         tick_ndecimals=2,
         x_tick_number=tick_number,
         y_tick_number=tick_number,
         # Grid
         grid=False, grid_color="lightgrey",
         # Labels
         x_label=x_label, x_label_size=15,
         y_label=y_label, y_label_size=15, y_label_rotation=y_label_rotation,
         x_label_pad=10,
         y_label_pad=10,
         # Legend
         plot_label=plot_label,
         legend=False,
         # Bounds
         y_upper_bound=y_bounds[1] if not isinstance(y_bounds, type(None)) else 0 if max(y) < 0 else None,
         y_lower_bound=y_bounds[0] if not isinstance(y_bounds, type(None)) else 0 if min(y) > 0 else None,
         x_upper_bound=x_bounds[1] if not isinstance(x_bounds, type(None)) else 0 if max(x) < 0 else None,
         x_lower_bound=x_bounds[0] if not isinstance(x_bounds, type(None)) else 0 if min(x) > 0 else None,
         x_upper_resize_pad=0, x_lower_resize_pad=0,
         y_upper_resize_pad=0, y_lower_resize_pad=0,
         # Other
         resize_axes=resize,
         zorder=zorder,
         # aspect=1/2500,
         )


def lpf(a):
    mean = a.mean()
    std = a.std()
    idxs = np.where(abs(a) > mean + 10 * std)
    a_f = np.delete(a, idxs)
    mean_f = a_f.mean()
    for idx in idxs:
        a[idx] = mean_f
    for i in range(0, len(a)-2):
        if abs(a[i]) > 100*abs(a[i+1]):
            a[i] = a[i+1]
        if abs(a[i]) > 100*abs(a[i+2]):
            a[i] = a[i+2]
    return a


def arc_length(x, y):
    npts = len(x)
    arc = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    for k in range(1, npts):
        arc = arc + np.sqrt((x[k] - x[k-1])**2 + (y[k] - y[k-1])**2)
    return arc


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


"""
=============================================
=============================================
=============================================
Data
=============================================
=============================================
=============================================
"""


# Constants
g = 9.80665

# Conversion
conv_torque = g/100


"""
Robot
"""


class Robot:

    # Constants
    g = 9.80665
    mu_s = 0.25

    # Vehicle parameters
    mass = 3.5                          # Kg
    # Mission parameters
    V = 3                               # m/s
    # Longitudinal
    l = 0.305                           # m
    l_f = 0.16                          # m
    l_r = 0.145                         # m
    # Axial                             # m
    w = 0.25                            # m
    l_axle = 0.125                      # m
    # Vertical
    h = 0.15                            # m
    cg_h = 0.125                        # m
    # Wheels
    w_w = 30*10**-3                     # m
    w_d = 113*10**-3                    # m
    w_diag = np.sqrt(w_w**2+w_d**2)     # m
    # Transmission
    d_trans = 0.02                      # m

    def N_f(self):
        return self.g*self.mass*self.l_r/self.l

    def F_xf(self):
        return self.mu_s*self.N_f()

    def F_yf(self):
        return self.F_xf()*np.tan(rad(self.delta_f))

    def toppling_delta_f(self, delta_f):
        self.delta_f = delta_f
        arm_n = self.w_w/2+self.l_axle/2
        S_M = self.g*self.mass*arm_n-self.cg_h*self.F_yf()
        return S_M

    def I_toppling(self):
        I_G = 1/3*self.mass*(self.w**2+self.h**2)
        d = np.sqrt((self.w/2)**2+(self.h/2)**2)
        return I_G+self.mass*d**2

    def toppling_psi(self, delta, psi_dot, t):
        """
        :param delta: Wheel rotation angle. Maximum: 40 degrees
        :param psi_dot: Angular velocity of the vehicle
        :param t: Time vector
        :return: Toppling angle theta and limit toppling angle theta: if (lim_theta + alpha) >90 -> toppling
        """
        # Safety factor
        SF_IG = 1
        # Moment of inertia
        I_G = self.I_toppling()/SF_IG
        # Velocity perpendicular to the path traced by the wheels at their rotation angle delta
        # Components:
        #   Velocity of the CG wrt toppling point due to motion not tangent to wheel rotation delta
        #   Velocity of the CG wrt toppling point due to angular velocity of the robot
        v_perp = self.V*np.cos(rad(90)-delta) - psi_dot*self.l_r*np.sin(rad(90)-delta)
        # Angle arctangent of CG height over half the axle length: from tipping point in wheel to CG (>90 -> topple)
        alpha = np.arctan(self.cg_h/(self.w_w+self.l_axle/2))
        # Distance from tipping point to CG
        a = np.sqrt(self.cg_h**2+(self.l_axle/2)**2)
        # Velocity perpendicular to the derivative of the toppling angle theta
        v_perp_theta_dot = v_perp/np.cos(alpha)
        # Derivative of toppling angle theta
        theta_dot = v_perp_theta_dot/a
        # ???
        theta_dot_f = theta_dot*(I_G+self.mass*(a*np.cos(alpha))**2)/(I_G+self.mass*a**2)
        # Integral to obtain theta
        theta = primitive(theta_dot_f, t[1]-t[0])
        # Limit
        theta_lim = rad(90) - alpha
        return deg(theta), deg(theta_lim)

    def w_I_z(self):
        m = 0.114
        d = self.w_d/2
        h = 0.565
        T = 8.9/10
        w_I_z = m*self.g*T**2*d**2/(4*np.pi**2*h)
        return w_I_z


"""
Disturbance
"""


class Disturbance:

    """
    Class variables:
        Wheel dimensions
        Bump constant
    """

    w_w = Robot().w_w                          # m
    w_h = Robot().w_d                          # m
    w_diag = Robot().w_diag                    # m

    B_c = 100*3                                # N

    def __init__(self, delta, d):
        """
        :param delta: Wheel rotation angle
        :param d: Disturbance function
        """
        self.delta = delta
        self.f = self.B_c*d

    def d(self):
        return self.w_diag/2*np.sin(self.delta+np.arctan(self.w_w/(self.w_h/2)))

    def F(self):
        return self.f*self.d()

    def M(self):
        return self.d()/2*self.F()


"""
Path planner
"""


class PathPlanner:

    # Vehicle parameters
    v = 3
    l = 0.305

    # Path parameters
    dx = 0.001
    dt = dx/v

    # Input
    X_60 = 9+15*np.cos(rad(60))
    Y_60 = 15*np.sin(rad(60))

    x_0 = np.array([0, 3, 6, 9])
    y_0 = np.zeros(len(x_0))
    x_60 = np.array([X_60])
    y_60 = np.array([Y_60])
    x_02 = np.array([X_60+4, X_60+6, X_60+8, X_60+10, X_60+12])
    y_02 = Y_60*np.ones(len(x_02))
    x_90 = np.array([X_60+12+1, X_60+12+3, X_60+12+8, X_60+12+24])
    y_90 = np.zeros(len(x_90))

    # Path
    x = np.concatenate((x_0, x_60, x_02, x_90))
    y = np.concatenate((y_0, y_60, y_02, y_90))

    # Path
    rx = np.arange(0, x[-1], dx)
    path = Rbf(x, y, smooth=0.01)(rx)
    t = np.linspace(0, arc_length(rx, path)/v, len(rx))

    # Psi
    psi = np.arctan(derivative(path, dx))
    psi = lpf(psi)

    v_x = v*np.cos(psi)

    # Psi_dot
    psi_dot = derivative(psi, dx)*v_x
    psi_dot = lpf(psi_dot)

    # Delta
    delta = np.arctan(l/v*psi_dot)
    delta = lpf(delta)

    # Omega
    omega = derivative(delta, dt)
    omega = lpf(omega)

    def f_path(self):
        fig = figure((12, 4))
        scatter(x=self.x, y=self.y, plot_label="Reference points",
                marker="x",
                point_size=30,
                color="#7aa9ff",
                zorder=0,
                resize_axes=False)
        plot_signal(x=self.rx, y=self.path, color="darkorange", plot_label="Path",
                    # Axes
                    x_label="x [m]",
                    y_label="y [m]",
                    # Ticks
                    tick_number=10,
                    # Bounds
                    x_bounds=[0, 54],
                    y_bounds=[-2, 16])
        import matplotlib.pyplot as plt
        # Contour plots
        x_0 = np.arange(0, 9, self.dx)
        y_0 = np.zeros(len(x_0))
        x_c60 = np.arange(9, self.X_60, self.dx)
        y_c60 = np.linspace(0, self.Y_60, len(x_c60))
        x_60 = np.arange(self.X_60, self.X_60+12, self.dx)
        y_60 = self.Y_60*np.ones(len(x_60))
        x_90 = np.arange(self.X_60+12, self.x_90[-1], self.dx)
        y_90 = np.zeros(len(x_90))

        x_ref = np.concatenate((x_0, x_c60, x_60, x_90))
        y_ref = np.concatenate((y_0, y_c60, y_60, y_90))

        plt.plot(x_ref, y_ref, label="Reference", linewidth=1, linestyle="--", zorder=0)

        # Other
        plt.gca().set_facecolor('#ffeed9')
        fig.patch.set_facecolor('#ffeed9')
        plt.legend(prop={'family': 'monospace'})
        plt.tight_layout()
        plt.show()

    def f_delta(self):
        fig = figure((12, 4))
        plot_signal(x=self.t, y=deg(self.psi), color="orange", plot_label="Ψ [deg]")
        plot_signal(x=self.t, y=deg(self.delta), color="green", plot_label="δ [deg]")
        plot_signal(x=self.t, y=deg(self.omega), plot_label="ω [deg s-1]",
                    # Axes
                    x_label="t [s]",
                    y_label="[deg]",
                    # Ticks
                    tick_number=13,
                    # Bounds
                    x_bounds=[0, 24],
                    y_bounds=[-110, 110])

        import matplotlib.pyplot as plt
        plt.legend(prop={'family': 'monospace'})
        plt.tight_layout()
        plt.show()

"""
Motor characteristic
"""


class MC:

    # Input voltage
    u_in = 6                         # V
    u_peak = 7.4                     # V

    # No load
    o_noload = rad(60)/0.09

    # Stall
    """
    Torque produced by mechanical device with output rotational speed 0
    """
    t_stall = 10.1*conv_torque       # N/m
    i_stall = 920*10**-3             # A

    # Standing torque
    """
    Torque required to force shaft out of position
    """
    t_standing = 10.6*conv_torque    # N/m
    i_running = 330*10**-3           # A

    # Idle
    i_idle = 2*10**-3                # A

    """
    Heat sink
    Servo dimensions:
        B = 38.72 mm
        H = 39.00 mm
        W = 19.00 mm
    """
    h = 15.00 * 10 ** -3
    w = 15.00 * 10 ** -3
    l = 35.00 * 10 ** -3
    heatsink_fin_thickness = 1
    nu = 0.15
    sf = 2
    # Mass
    d_alu6082 = 2700

    def k_t(self):
        return self.t_stall/self.i_stall

    def k_s(self):
        return self.o_noload/self.u_peak

    def R_arm(self):
        return self.u_in/self.i_stall

    def omega(self, torque):
        return self.k_s()*(self.u_in-torque*self.R_arm()/self.k_t())

    def i(self, n_ticks):
        t = np.linspace(-self.t_stall, self.t_stall, n_ticks)
        return t/self.k_t()

    def n_heatsink_slots(self):
        return (self.h*10**3-1)/2

    def heat_transferred(self):
        """
        Aluminium 6086
        """
        u = 180                      # W/m2*K
        dt = 60                      # K
        return self.nu*u*dt*self.heatsink_area()/self.sf

    def i_max_thermal(self):
        return np.sqrt(self.heat_transferred()/self.R_arm())

    def t_max_thermal(self):
        return self.k_t()*self.i_max_thermal()

    def forward_motoring(self):
        t = np.linspace(0, self.t_stall, 1000)
        o = self.omega(t)
        return t, o

    def forward_braking(self):
        t = np.linspace(-self.t_stall, 0, 1000)
        # o = max(self.forward_motoring()[1])*np.ones(1000)
        # o = self.forward_motoring()[1][::-1]
        o = self.omega(t)
        return t, o

    def reverse_braking(self):
        t = np.linspace(0, self.t_stall, 1000)
        # o = -max(self.forward_motoring()[1])*np.ones(1000)
        # o = -self.forward_motoring()[1]
        o = -self.omega(t)[::-1]-max(self.forward_motoring()[1])
        return t, o

    def reverse_motoring(self):
        t = np.linspace(-self.t_stall, 0, 1000)
        o = self.omega(t)-2*max(self.forward_motoring()[1])
        return t, o

    def heatsink_area(self):
        return self.l*(2*self.h+2*self.w+self.n_heatsink_slots()*2/3*self.w)

    def heatsink_volume(self):
        return self.l*(self.h*self.w-2*self.n_heatsink_slots()*self.w/3*1/(2*self.n_heatsink_slots()+1)*self.h)

    def heatsink_mass(self):
        return self.d_alu6082*self.heatsink_volume()


"""
Load characteristic
"""


class LC:

    t = PathPlanner.t
    psi, psi_dot = PathPlanner.psi, PathPlanner.psi_dot
    delta_f, omega = PathPlanner.delta, PathPlanner.omega

    def torque_omega_dot(self):
        omega_dot = derivative(self.omega, self.t[1] - self.t[0])
        torque_omega = Robot().w_I_z() * omega_dot * 2
        # Gear ratio
        torque_omega = torque_omega/np.cos(self.delta_f)
        return torque_omega

    def torque_disturbance(self):
        torque_disturbance = 2 * Disturbance(delta=self.delta_f, d=self.t[1] - self.t[0]).M()
        # Gear ratio
        torque_disturbance = torque_disturbance/np.cos(self.delta_f)
        return torque_disturbance

    def toppling(self, cb_max):
        toppling_psi = Robot().toppling_psi(self.delta_f, self.psi_dot, self.t)
        ratio = min(1 - (cb_max - toppling_psi[1]) / cb_max, 1)
        darkred = create_cmap(252, 152, 3, 252, 152, 3)
        cmap = combine_cmaps("RdBu_r", darkred, cmap1_share=ratio)
        return toppling_psi, cmap

    def plot(self, saturation=True):
        SF_torque = 30
        SF_omega = 4
        SF_toppling = 200

        torque = self.torque_omega_dot() + self.torque_disturbance()

        # Toppling
        cb_max = 35
        theta, theta_max = self.toppling(cb_max)[0]
        line(x=SF_torque * torque, y=SF_omega * self.omega,
             # color="black",
             norm=SF_toppling*theta, cmap="RdBu_r",
             line_width=1.5,
             # Color bar
             color_bar=True, cb_pad=0.1, cb_top_title=True, shrink=0.5,
             cb_title=" Toppling \nlikelyhood", x_cb_top_title=0, cb_title_size=12.5, cb_top_title_pad=20,
             cb_vmin=-cb_max, cb_vmax=cb_max, cb_hard_bounds=False, cb_tick_number=3,
             # Title, labels
             title="",
             x_label="T [Nm]", x_label_size=15, x_label_pad=5,
             y_label="ω [rad s-1]", y_label_rotation=90, y_label_size=15, y_label_pad=5,
             # Ticks
             tick_ndecimals=2, tick_label_size=10,
             x_tick_number=10, y_tick_number=15,
             # Axes
             resize_axes=False,
             # Grid
             grid=False, grid_color="lightgrey",
             )

        import matplotlib.pyplot as plt
        plt.gca().collections[-1].colorbar.ax.set_yticklabels(['High θ<0', '0', 'High θ>0'], font="monospace")
        # plt.tight_layout()
        # plt.show()

    def plot_moment(self):
        fig = figure((10, 4))
        plot_signal(self.t, self.torque_disturbance()*1000,
                    plot_label="Disturbance",
                    color="darkred", zorder=2)
        plot_signal(self.t[:-2], moving_average(self.torque_omega_dot(), 3)*1000,
                    plot_label="Steering",
                    color="#fcdc9a", zorder=1)
        plot_signal(self.t[:-2], moving_average((self.torque_omega_dot()+self.torque_disturbance()), 3)*1000,
                    plot_label="Total",
                    color="darkblue", zorder=0,
                    # Axes
                    x_bounds=[0, 24],
                    y_bounds=[-6, 6],
                    # Labels
                    x_label="t [s]",
                    y_label="T [mNm]")
        import matplotlib.pyplot as plt
        plt.legend(prop={'family': 'monospace'})
        plt.tight_layout()
        plt.show()

    def plot_gear_ratio(self):
        fig = figure((6, 4))
        plot_signal(self.t, np.cos(self.delta_f),
                    # Labels
                    x_label="t [s]",
                    y_label="GR [-]",
                    # Ticks
                    tick_number=6,
                    # Axes
                    x_bounds=[0, 24],
                    y_bounds=[0, 2])
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.show()



"""
=============================================
=============================================
=============================================
Plot
=============================================
=============================================
=============================================
"""


class Plot:

    mc = MC()
    fig = figure((15, 10))
    n_ticks = 3
    tick_label_size = 10
    axis_font_size = 15
    axis_title_pad = 10

    def reaction(self):
        self.y_bounds = [-100, 100]
        self.torque_bound = 13
        self.torque_bound_factor = self.torque_bound/max(self.mc.forward_motoring()[0])
        self.main()

    def reaction_s(self):
        self.saturation = True
        self.n_ticks = 17
        self.y_bounds = [-20, 20]
        self.torque_bound = self.mc.forward_motoring()[0].max() / (self.mc.forward_braking()[1].max()/20)
        self.torque_bound_factor = self.torque_bound/max(self.mc.forward_motoring()[0])
        self.main()

    def main(self):
        import matplotlib.pyplot as plt

        self.basic(x=self.mc.forward_motoring()[0], y=self.mc.forward_motoring()[1],
                   color="darkred")
        self.basic(x=self.mc.forward_braking()[0], y=self.mc.forward_braking()[1],
                   color="darkred")
        self.basic(x=self.mc.reverse_braking()[0], y=self.mc.reverse_braking()[1],
                   color="darkred")

        self.zero_lines()

        self.heat_lines()

        self.fill_continous_operation()

        self.fill_intermittent_operation()

        LC().plot()

        self.style(x=self.mc.reverse_motoring()[0], y=self.mc.reverse_motoring()[1],
                   color="darkred")

        plt.xticks(np.linspace(-max(self.mc.forward_motoring()[0]), max(self.mc.forward_motoring()[0]), self.n_ticks),
                   fontname="serif", fontsize=self.tick_label_size)

        self.second_axis()

        plt.show()

    def basic(self, x, y, color):
        line(x=x, y=y, color=color,
             line_width=2,
             spines_removed=[],
             fig=self.fig, )

    def style(self, x, y, color):
        line(x=x, y=y, color=color,
             line_width=2,
             x_bounds=[- self.torque_bound, self.torque_bound], x_upper_resize_pad=0, x_lower_resize_pad=0,
             y_bounds=self.y_bounds,
             y_upper_resize_pad=0, y_lower_resize_pad=0,
             y_custom_tick_locations=[self.mc.forward_braking()[1].max(), self.mc.reverse_braking()[1].min()],
             spines_removed=["top", "right"],
             x_tick_number=self.n_ticks, y_tick_number=self.n_ticks,
             tick_ndecimals=2,
             x_tick_label_size=self.tick_label_size, y_tick_label_size=self.tick_label_size,
             grid=True, grid_color="lightgrey", grid_lines="--",
             title="",
             x_label="T [Nm]", x_label_size=self.axis_font_size,
             y_label="ω [rad s-1]", y_label_size=self.axis_font_size, y_label_rotation=90,
             x_label_pad=self.axis_title_pad, y_label_pad=5,
             fig=self.fig,
             resize_axes=True
             )

    def second_axis(self):
        """
        Second axis
        """
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FormatStrFormatter
        ax2 = plt.gca().twiny()
        ax2.set_xlim(left=-0.920*self.torque_bound_factor, right=0.920*self.torque_bound_factor)
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.xticks(self.mc.i(self.n_ticks), fontname="serif", fontsize=self.tick_label_size)
        ax2.set_title("I [A]", fontname="serif", fontsize=self.axis_font_size, pad=self.axis_title_pad)

    def zero_lines(self):
        """
        Zero lines
        """
        import matplotlib.pyplot as plt
        plt.axvline(0, color="grey", linestyle="--")
        plt.axhline(0, color="grey", linestyle="--")

    def heat_lines(self):
        """
        Heat lines
        """
        import matplotlib.pyplot as plt
        plt.axvline(self.mc.t_max_thermal(), color="red", linestyle="-")
        plt.axvline(-self.mc.t_max_thermal(), color="red", linestyle="-")

    def fill_continous_operation(self):
        # Thermal limit intersection
        limit = self.mc.t_max_thermal()
        idx_low = find_nearest_idx(self.mc.forward_braking()[0], -limit)
        idx_high = find_nearest_idx(self.mc.forward_motoring()[0], limit)
        x = np.concatenate((self.mc.forward_braking()[0][idx_low::], self.mc.forward_motoring()[0][::idx_high]))
        y = np.concatenate((self.mc.forward_braking()[1][idx_low::], self.mc.forward_motoring()[1][::idx_high]))
        z = np.concatenate((self.mc.reverse_motoring()[1][idx_low::], self.mc.reverse_braking()[1][::idx_high]))
        fill_area(x=x,
                  y=y,
                  z=z,
                  between=True,
                  color="#c7ffd6",
                  resize_axes=False,
                  zorder=0)

    def fill_intermittent_operation(self):
        # Thermal limit intersection
        limit = self.mc.t_max_thermal()
        idx_low = find_nearest_idx(self.mc.forward_braking()[0], -limit)
        idx_high = find_nearest_idx(self.mc.forward_motoring()[0], limit)
        x_low = self.mc.forward_braking()[0][:idx_low]
        y_low = self.mc.forward_braking()[1][:idx_low]
        z_low = self.mc.reverse_motoring()[1][:idx_low]
        fill_area(x=x_low,
                  y=y_low,
                  z=z_low,
                  between=True,
                  color="darkred",
                  resize_axes=False,
                  zorder=0)
        x_high = self.mc.forward_motoring()[0][idx_high:]
        y_high = self.mc.forward_motoring()[1][idx_high:]
        z_high = self.mc.reverse_braking()[1][idx_high:]
        fill_area(x=x_high,
                  y=y_high,
                  z=z_high,
                  between=True,
                  color="darkred",
                  resize_axes=False,
                  zorder=0)


Plot().reaction_s()
