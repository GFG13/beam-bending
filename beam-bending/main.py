# import 3rd party libraries
import os
import sys
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# import local library
sys.path.insert(0, os.path.abspath('../beam-bending/beam-bending/'))
import beam_formulae as bf
import constants as con
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_excel('../data/4pt_test-results_20200611.xlsx', sheet_name='test_data_ottawa')
df.drop(df.columns[22], axis=1, inplace=True)
df_G = df[df['quality'] == 'G']
df_G.loc[:, ["init_load", "add_load", "max_load", "peak_force"]] = df_G[
    ["init_load", "add_load", "max_load", "peak_force"]].apply(pd.to_numeric)

# DISTRIBUTED LOAD FROM SELF-WEIGHT

# L_rock = df_G["L_left"]+df_G["L_right"]
d_init = ((df_G["dia_left"] + df_G["dia_right"]) / 2) / 1000
df_G = df_G.assign(w_rock=bf.circle_area(d_init) * con.rho_rock * con.grav)  # [N/m]
df_G = df_G.assign(w_ice=bf.circle_area(d_init) * con.rho_ice * con.grav)  # [N/m]

# RESULTANT LOADS
# using larger rock core for greatest resultant force (negligble difference)

df_G = df_G.assign(
    P_rock=bf.p_result(df_G["w_rock"],
                       0.001 * np.where(df_G["L_left"] >= df_G["L_right"], df_G["L_left"], df_G["L_right"])))  # [N]
df_G = df_G.assign(
    P_ice=bf.p_result(df_G["w_ice"], 0.001 * df_G["post-freeze_aperture"]))  # [N]

# df1 = df1.assign(e=pd.Series(np.random.randn(sLength)).values)

# REACTION FORCES
# self-weight +applied load (single support)
df_G = df_G.assign(R=df_G["P_rock"] + (df_G["P_ice"] / 2) + (df_G["peak_force"]))

M = bf.moment(df_G["R"], (0.5 * con.P_span / 1000 - 0.5 * (0.001 * df_G["post-freeze_aperture"]))) \
    - bf.moment(df_G["P_rock"], (0.001 * np.where(df_G["L_left"] >= df_G["L_right"], df_G["L_left"], df_G["L_right"]))) \
    - bf.moment(con.P, ((1 / 6 * con.P_span / 1000) - 0.5 * (0.001 * df_G["post-freeze_aperture"])))

# COMPUTE MAXIMUM TENSILE STRESS
df_G["peak_stressMPa"] = bf.stress(M, d_init / 2) / 1e6
# print("Tensile stress at ice-rock interface: ", round((df_G["peak_stressMPa"]),3), "MPa")


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('../data/sig_t-output.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df_G.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
