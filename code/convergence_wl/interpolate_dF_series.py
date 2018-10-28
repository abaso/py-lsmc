import numpy as np
from scipy.interpolate import interp1d
from sys import argv

# Command line arguments
input_fname = argv[1]
freq = int(argv[2])

# Load dF series
input_data = np.loadtxt(input_fname)

# Unpack
sweeps = np.cumsum(input_data[:,0])
dF = input_data[:,1]
err = input_data[:,2]

# Create functions by linear interpolation
dF_func = interp1d(sweeps, dF, kind='quadratic')
err_func = interp1d(sweeps, err, kind='quadratic')

# Array of sweeps for frequency we want
new_sweeps = np.arange(freq, sweeps[-1], freq)

# Where does our data actually begin?
start = sweeps[0] + freq - sweeps[0]%freq
inlimits = np.array(new_sweeps >= start)

# Initialise new arrays for interpolated values
new_dF = np.zeros(len(new_sweeps))
new_err = np.zeros(len(new_sweeps))

# NaN's for entries before the data series
new_dF[ ~inlimits ] = np.nan
new_err[ ~inlimits ] = np.nan

# Array of interpolated values
new_dF[ inlimits ] = dF_func(new_sweeps[ inlimits ])
new_err[ inlimits ] = err_func(new_sweeps[ inlimits ])

# Save a new deltaF file
data_to_save = np.zeros( (len(new_sweeps), 3) )
data_to_save[:,0] = np.ones(len(new_sweeps)) * freq # save sweeps per iter, not cumulative
data_to_save[:,1] = new_dF
data_to_save[:,2] = new_err
np.savetxt("new_"+input_fname, data_to_save)

