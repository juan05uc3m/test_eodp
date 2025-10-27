
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\juant\\EODP_DATA\\eodp_students-master\\auxiliary'
#indir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-L1B\\input"
indir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-ISM\\myoutputismc"
outdir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-L1B\\myputputs_with_ism_imput"

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
