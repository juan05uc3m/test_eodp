
# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\juant\\EODP_DATA\\eodp_students-master\\auxiliary'
#indir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-ISM\\input\\gradient_alt100_act150"
indir = r"C:\\Users\\juant\\EODP_DATA\\EODP-TS-E2E\\sgm_out"
outdir = r"C:\\Users\\juant\\EODP_DATA\\\EODP-TS-ISM\\myoutputism"

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()



