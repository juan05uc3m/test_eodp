from common.io.writeToa import writeToa, readToa
import numpy as np
import matplotlib.pyplot as plt

#Resultados suyos
toa_ref_0 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\output", "l1b_toa_VNIR-0.nc")
toa_ref_1 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\output", "l1b_toa_VNIR-1.nc")
toa_ref_2 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\output", "l1b_toa_VNIR-2.nc")
toa_ref_3 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\output", "l1b_toa_VNIR-3.nc")


#Con ganancia incluida
toa_0 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-0.nc")
toa_1 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-1.nc")
toa_2 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-2.nc")
toa_3 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs", "l1b_toa_VNIR-3.nc")

#Señal que te llega
toa_isrf_0 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-0.nc")
toa_isrf_1 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-1.nc")
toa_isrf_2 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-2.nc")
toa_isrf_3 = readToa(r"C:\\Users\juant\EODP_DATA\\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-3.nc")


#Los resultados no ecualizados
toa_0_no_eq = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-0.nc")
toa_1_no_eq = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-1.nc")
toa_2_no_eq = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-2.nc")
toa_3_no_eq = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-L1B\myoutputs_no_eq", "l1b_toa_VNIR-3.nc")

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
    print(f"Banda {i}: media={mu:.3f}, sigma={sigma:.3f}, límite_3σ={thr:.3f}, Cumple={ok}")




# Listas con restaurados y ISRF
toa_restored_list = [toa_0, toa_1, toa_2, toa_3]
toa_isrf_list     = [toa_isrf_0, toa_isrf_1, toa_isrf_2, toa_isrf_3]

# Central ALT (fila central = 50)
alt_central = toa_0.shape[0] // 2  # 100 // 2 = 50

for i, (toa_band, toa_isrf_band) in enumerate(zip(toa_restored_list, toa_isrf_list)):
    # Extraer la línea central ALT (dim 0 = ALT, dim 1 = espectral)
    restored = toa_band[alt_central, :]
    isrf     = toa_isrf_band[alt_central, :]

    # Crear nueva figura para cada banda
    plt.figure(figsize=(10,6))
    plt.plot(restored, label=f"Restored (l1b_toa) - Banda {i}", linewidth=2)
    plt.plot(isrf, label=f"After ISRF (ism_toa_isrf) - Banda {i}", linestyle="--", linewidth=2)
    plt.xlabel("Índice espectral (150 píxeles)")
    plt.ylabel("TOA Radiance (a.u.)")
    plt.title(f"Comparación Banda {i} - Línea ALT central ({alt_central})")
    plt.legend()
    plt.grid(True)

plt.show(block=False)
# --- Comparación resultados míos vs no ecualizados ---

# Central ALT (fila central)
alt_central = toa_0.shape[0] // 2  # 100 // 2 = 50

for i in range(4):
    # Selección de bandas con if/elif (evitando zip/listas si quieres hacerlo explícito)
    if i == 0:
        mine   = toa_0[alt_central, :]
        no_eq  = toa_0_no_eq[alt_central, :]
    elif i == 1:
        mine   = toa_1[alt_central, :]
        no_eq  = toa_1_no_eq[alt_central, :]
    elif i == 2:
        mine   = toa_2[alt_central, :]
        no_eq  = toa_2_no_eq[alt_central, :]
    elif i == 3:
        mine   = toa_3[alt_central, :]
        no_eq  = toa_3_no_eq[alt_central, :]

    # Gráfico comparativo
    plt.figure(figsize=(10,6))
    plt.plot(mine, label=f"Mis resultados (Banda {i})", linewidth=2)
    plt.plot( no_eq, label=f"No ecualizado (Banda {i})", linestyle="--", linewidth=2)
    plt.xlabel("Índice espectral (150 píxeles)")
    plt.ylabel("TOA Radiance (a.u.)")
    plt.title(f"Comparación Mis Resultados vs No-EQ - Banda {i} (ALT central={alt_central})")
    plt.legend()
    plt.grid(True)

plt.show()