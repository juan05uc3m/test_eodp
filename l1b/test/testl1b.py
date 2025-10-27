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
    diff_flat = diff.flatten()

    # Cuántos píxeles tienen diferencia < tol
    count_below_tol = np.sum(diff_flat < tol)

    # Cálculo de media y sigma para evaluar el 3-sigma
    mu = np.mean(diff_flat)
    sigma = np.std(diff_flat)
    threshold = mu + 3 * sigma

    ok = threshold < tol
    return ok, count_below_tol

# --- Comparación l1b_toa ---
print("\nComparison l1b_toa\n")
for i, (my, ref) in enumerate([
    (toa_0, toa_ref_0),
    (toa_1, toa_ref_1),
    (toa_2, toa_ref_2),
    (toa_3, toa_ref_3)
]):
    ok, count = check_band(my, ref)
    print(f"Band {i}: {'meets the condition' if ok else 'do not meet the condition'}")
    print(f"Number of pixels with < 0.01%: {count}\n")


# Listas con restaurados y ISRF
toa_restored_list = [toa_0, toa_1, toa_2, toa_3]
toa_isrf_list     = [toa_isrf_0, toa_isrf_1, toa_isrf_2, toa_isrf_3]

# Central ALT (fila central = 50)
alt_central = toa_0.shape[0] // 2  # 100 // 2 = 50

"""
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

"""

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
bands_mine = [toa_0, toa_1, toa_2, toa_3]
bands_noeq = [toa_0_no_eq, toa_1_no_eq, toa_2_no_eq, toa_3_no_eq]
titles = ["VNIR-0", "VNIR-1", "VNIR-2", "VNIR-3"]


for ax, mine, no_eq, title in zip(axs.flat, bands_mine, bands_noeq, titles):
    ax.plot(mine[alt_central, :], label="My result", linewidth=2)
    ax.plot(no_eq[alt_central, :], label="No equalized", linewidth=1, color="r")
    ax.set_title(f"Band {title} (ALT={alt_central})")
    ax.set_xlabel("Spectral index (pixels)")
    ax.set_ylabel("TOA Radiance (a.u.)")
    ax.legend()
    ax.grid(True)

fig.suptitle("Comparison: My results vs No-Equalized (All VNIR Bands)", fontsize=14)
plt.tight_layout()
plt.show()





# --- Comparación resultados míos vs no ecualizados ---

# Central ALT (fila central)
alt_central = toa_0.shape[0] // 2  # 100 // 2 = 50


""""
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
"""

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
bands_restored = [toa_0, toa_1, toa_2, toa_3]
bands_isrf = [toa_isrf_0, toa_isrf_1, toa_isrf_2, toa_isrf_3]

for ax, restored, isrf, title in zip(axs.flat, bands_restored, bands_isrf, titles):
    ax.plot(restored[alt_central, :], label="Restored (L1B TOA)", linewidth=2)
    ax.plot(isrf[alt_central, :], label="After ISRF (ISM TOA)", linewidth=1,color="r")
    ax.set_title(f"Band {title} (ALT={alt_central})")
    ax.set_xlabel("Spectral index (pixels)")
    ax.set_ylabel("TOA Radiance (a.u.)")
    ax.legend()
    ax.grid(True)

fig.suptitle("Comparison: Restored vs ISRF (All VNIR Bands)", fontsize=14)
plt.tight_layout()
plt.show()


#comparando todas:
# Listas de datos por banda
bands_noeq = [toa_0_no_eq, toa_1_no_eq, toa_2_no_eq, toa_3_no_eq]
bands_eq = [toa_0, toa_1, toa_2, toa_3]
bands_isrf = [toa_isrf_0, toa_isrf_1, toa_isrf_2, toa_isrf_3]

# Crear figura 2x2 (una por banda)
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

for ax, noeq, eq, isrf, title in zip(axs.flat, bands_noeq, bands_eq, bands_isrf, titles):
    ax.plot(noeq[alt_central, :], label="No equalized", linewidth=1, color= "r")
    ax.plot(eq[alt_central, :], label="Equalized", linewidth=1, color="black")
    ax.plot(isrf[alt_central, :], label="After ISRF", linewidth=1)

    ax.set_title(f"Band {title} (ALT={alt_central})")
    ax.set_xlabel("Spectral index (pixels)")
    ax.set_ylabel("TOA Radiance (a.u.)")
    ax.legend()
    ax.grid(True)

fig.suptitle("Comparison: No Equalized vs Equalized vs ISRF (All VNIR Bands)", fontsize=14)
plt.tight_layout()
plt.show()