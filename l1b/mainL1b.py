
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\juant\\EODP_DATA\\eodp_students-master\\auxiliary'
#indir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-L1B\\input"
outdir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-L1B\\myoutputs_with_ism_input"

#Ahora usare la salida del ISM como entrada del módulo 1lb
#El output lo cambio para que sea output con entrada del ism
indir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-ISM\\myoutputism"

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
