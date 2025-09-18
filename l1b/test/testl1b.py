from common.io.writeToa import writeToa, readToa
import numpy as np


#Con ganancia incluida
toa_ref_0 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\output", "l1b_toa_VNIR-0.nc")
toa_ref_1 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\output", "l1b_toa_VNIR-1.nc")
toa_ref_2 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\output", "l1b_toa_VNIR-2.nc")
toa_ref_3 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\output", "l1b_toa_VNIR-3.nc")


#Con ganancia incluida
toa_0 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-0.nc")
toa_1 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-1.nc")
toa_2 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-2.nc")
toa_3 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-3.nc")

#Señal que te llega
toa_isrf_0 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-0.nc")
toa_isrf_1 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-1.nc")
toa_isrf_2 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-2.nc")
toa_isrf_3 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-3.nc")


#Resultados ecualizados
toa_0_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_eq_VNIR-0.nc")
toa_1_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_eq_VNIR-1.nc")
toa_2_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_eq_VNIR-2.nc")
toa_3_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_eq_VNIR-3.nc")

#Los resultados no ecualizados
toa_0_no_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-0.nc")
toa_1_no_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-1.nc")
toa_2_no_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-2.nc")
toa_3_no_eq = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-3.nc")

#APARTADO1
def check_band(toa_my, toa_ref, tol=0.01):
    # Diferencia relativa en porcentaje
    diff = np.abs(toa_my - toa_ref) / np.maximum(toa_ref, 1e-12) * 100

    # Media y sigma
    mu = np.mean(diff)
    sigma = np.std(diff)

    # Límite 3-sigma
    threshold = mu + 3*sigma

    # ¿Está por debajo del 0.01%?
    ok = threshold < tol
    return mu, sigma, threshold, ok

for i, (my, ref) in enumerate([(toa_0, toa_ref_0), (toa_1, toa_ref_1),
                               (toa_2, toa_ref_2), (toa_3, toa_ref_3)]):
    mu, sigma, thr, ok = check_band(my, ref)
    print(f"Banda {i}: media={mu:.6f}%, sigma={sigma:.6f}%, límite_3σ={thr:.6f}%, OK={ok}")



