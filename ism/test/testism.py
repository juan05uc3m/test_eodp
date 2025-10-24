#En este archivo se realizará un test de los resultados obtenidos en el módulo ism
from common.io.writeToa import writeToa, readToa
import numpy as np
import matplotlib.pyplot as plt

#Cargo los outputs suyos
toa_ism_isrf_0 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-0.nc")
toa_ism_isrf_1 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-1.nc")
toa_ism_isrf_2  = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-2.nc")
toa_ism_isrf_3  = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_isrf_VNIR-3.nc")

#cargo mis outputs

toa_ism_isrf_0_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_isrf_VNIR-0.nc")
toa_ism_isrf_1_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_isrf_VNIR-1.nc")
toa_ism_isrf_2_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_isrf_VNIR-2.nc")
toa_ism_isrf_3_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_isrf_VNIR-3.nc")


#Ahora cargo los ism opticos de sus outputs y de mis ooutputs

toa_ism_opt_0 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_optical_VNIR-0.nc")
toa_ism_opt_1 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_optical_VNIR-1.nc")
toa_ism_opt_2 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_optical_VNIR-2.nc")
toa_ism_opt_3 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_optical_VNIR-3.nc")

#los mios

toa_ism_opt_0_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_optical_VNIR-0.nc")
toa_ism_opt_1_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_optical_VNIR-1.nc")
toa_ism_opt_2_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_optical_VNIR-2.nc")
toa_ism_opt_3_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia3", "ism_toa_optical_VNIR-3.nc")


#Ahora hay que comprobar si tienen error
#utilizo la misma funcion que en 1lb

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


# --- Comparación ism_toa_isrf ---
print("\nComparison ism_toa_isrf\n")
for i, (my, ref) in enumerate([
    (toa_ism_isrf_0_juan, toa_ism_isrf_0),
    (toa_ism_isrf_1_juan, toa_ism_isrf_1),
    (toa_ism_isrf_2_juan, toa_ism_isrf_2),
    (toa_ism_isrf_3_juan, toa_ism_isrf_3)
]):
    ok, count = check_band(my, ref)
    print(f"Band {i}: {'meets the condition' if ok else 'do not meet the condition'}")
    print(f"Number of pixels with < 0.01%: {count}\n")


# --- Comparación ism_toa_optical ---
print("\n=== Comparison ism_toa_optical ===\n")
for i, (my, ref) in enumerate([
    (toa_ism_opt_0_juan, toa_ism_opt_0),
    (toa_ism_opt_1_juan, toa_ism_opt_1),
    (toa_ism_opt_2_juan, toa_ism_opt_2),
    (toa_ism_opt_3_juan, toa_ism_opt_3)
]):
    ok, count = check_band(my, ref)
    print(f"Band {i}: {'meets the condition' if ok else 'do not meet the condition'}")
    print(f"Number of pixels with < 0.01%: {count}\n")




# ---------- Visualización del efecto de borde (ejemplo banda 0) ----------

# Mostramos antes y después del filtro óptico
plt.figure()

plt.subplot(1,2,1)
plt.imshow(toa_ism_isrf_2)
plt.title("Before MTF filter (ISRF stage)")
plt.colorbar()

plt.subplot(1,2,2)
plt.imshow(toa_ism_opt_2)
plt.title("After MTF filter (Optical stage)")
plt.colorbar()

plt.show()

# ---------- Mapa de diferencias ----------
diff = toa_ism_opt_2 - toa_ism_isrf_2

plt.figure()
plt.imshow(diff, cmap='seismic', vmin=-0.01, vmax=0.01)
plt.title("Difference (Optical - ISRF)")
plt.colorbar(label="Radiance difference")
plt.show()

# ---------- Perfiles en el centro y cerca del borde ----------
row_center = toa_ism_opt_0.shape[0] // 2
row_edge = 5  # fila cercana al borde superior

plt.figure(figsize=(8,4))
plt.plot(toa_ism_isrf_2[row_center, :], label="Before MTF - Center")
plt.plot(toa_ism_opt_2[row_center, :], label="After MTF - Center")
plt.legend()
plt.title("Central row comparison")
plt.xlabel("Pixel column")
plt.ylabel("TOA value")
plt.show()

plt.figure(figsize=(8,4))
plt.plot(toa_ism_isrf_2[row_edge, :], label="Before MTF - Edge")
plt.plot(toa_ism_opt_2[row_edge, :], label="After MTF - Edge")
plt.legend()
plt.title("Edge row comparison (Border effect)")
plt.xlabel("Pixel column")
plt.ylabel("TOA value")
plt.show()



#SINCE THIS POINT I WILL MAKE THE ISM-0002 TEST


#Loading her outputs...
toa_ism_0 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_VNIR-0.nc")
toa_ism_1 = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_VNIR-1.nc")
toa_ism_2  = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_VNIR-2.nc")
toa_ism_3  = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\output", "ism_toa_VNIR-3.nc")

#Loading my outputs....

toa_ism_0_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia4", "ism_toa_VNIR-0.nc")
toa_ism_1_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia4", "ism_toa_VNIR-1.nc")
toa_ism_2_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia4", "ism_toa_VNIR-2.nc")
toa_ism_3_juan = readToa(r"C:\\Users\juant\EODP_DATA\EODP-TS-ISM\myoutputdia4", "ism_toa_VNIR-3.nc")


#AP1, we need to find out if our outputs are correct


# --- Comparación ism_toa_isrf ---
print("\nComparison ism_toa_VNIR\n")
for i, (my, ref) in enumerate([
    (toa_ism_0_juan, toa_ism_0),
    (toa_ism_1_juan, toa_ism_1),
    (toa_ism_2_juan, toa_ism_2),
    (toa_ism_3_juan, toa_ism_3)
]):
    ok, count = check_band(my, ref)
    print(f"Band {i}: {'meets the condition' if ok else 'do not meet the condition'}")
    print(f"Number of pixels with < 0.01%: {count}\n")



