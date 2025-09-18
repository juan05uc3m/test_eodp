from common.io.writeToa import writeToa, readToa

#Señal que te llega
toa_isrf_0 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-0.nc")
toa_isrf_1 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-1.nc")
toa_isrf_2 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-2.nc")
toa_isrf_3 = readToa("C:\\Users\juantej\PycharmProjects\EODP_TER_2021-20250918T152656Z-1-001\EODP_TER_2021\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-3.nc")

#Con ganancia incluida
toa_0 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-0.nc")
toa_1 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-1.nc")
toa_2 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-2.nc")
toa_3 = readToa("C:\\Users\juantej\PycharmProjects\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-3.nc")


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
