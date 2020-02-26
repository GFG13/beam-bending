import scipy.constants as sc

grav = sc.g;                # [m/s^2] gravity
total_span = 150;           # [mm] beam span
P_span = 1/3*total_span;    # [mm] loading span

d_init = .038               # [m]
x_rock = 0.15               # [m]
x_ice = 0.01                # [m]
rho_rock = 2600             # [kg/m3]
rho_ice = 1000              # [kg/m3]
P = 50*grav                 # [N]
