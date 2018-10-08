"""
Routines to read in postprocessed HiFi simulation results.

Notes 
----- 
The directory specified in postpath should include contents such as
grid_00000.h5, post_00000.h5, post_00000.xmf, ...

Sample Usage
------------
The following commands will allow access to the grid and the HDF5
files, and provide the time of each data file.

    import hifipy as hfp
    postpath = "~/HiFi_Runs/20161020a_LaminarBaseRun_LoRes/post_out_4_4"
    x, y, xx, yy = hfp.read_grid(postpath)
    file_list, time = hfp.read_directory(postpath)

To see the keys that are contained in each of the HDF5 files, use

    file_list[0].keys()

The first key will typically be "U01".  To get a slice of the "U01" in
the third output file, use 

    file_list[2]["U01"][:,0]
"""

from __future__ import print_function
from os.path import expanduser,isdir, isfile

import h5py
import numpy as np
import glob


def read_grid(postpath='.'):   
    """
    Reads in grid information from a HiFi simulation.  

    Inputs
    ------
    The sole input, postpath, must be a directory that contains the
    output files from a HiFi simulation, including a grid file such as 
    grid_00000.h5.  

    Sample usage
    ------------
    x, y, xx, yy = hifipy.read_grid('~/HiFi_Runs/20161020a_LaminarBaseRun_LoRes')
    """
    assert isdir(expanduser(postpath)), \
        "read_grid: The input must be a directory."
    
    files_grid = glob.glob(postpath+'/grid*.h5') 
    
    assert len(files_grid) > 0, \
        "read_grid: Grid file not found. Are you using the correct directory when calling read_grid?"

    files_grid.sort()

    gridfile = files_grid[0]
    grid = h5py.File(gridfile,'r')

    x_2D, y_2D = np.array(grid['U01']), np.array(grid['U02'])
    x_1D, y_1D = np.array(x_2D[0,:]), np.array(y_2D[:,0])

    return x_2D, y_2D, x_1D, y_1D    


def find_files_and_time(postpath='.'):
    """
    Creates a list of the HDF5 and xmf files in a directory, and reads
    in the time from the xmf files into an array.

    Sample usage
    ------------
    files_h5, files_xmf, time = find_files_and_time('.')

    Notes
    -----
    The time calculation is sensitive to the format of the xmf files.
    If that format changes, then this routine will have to be
    modified.
    """
    assert isdir(expanduser(postpath)), \
        "find_files_and_time: The input must be a directory."

    files_h5 = glob.glob(postpath+'/post*.h5')  ; files_h5.sort()
    files_xmf = glob.glob(postpath+'/post*.xmf') ; files_xmf.sort()
    nfilemax = len(files_h5)

    # Extract the time from the xmf files
    
    time = np.zeros(nfilemax)

    try:
        for i in range(0,nfilemax):
            file_xmf = open(files_xmf[i],'r')
            lines = file_xmf.readlines()                            
            time[i] = np.double(lines[5][18:30])
    except:
        print("find_files_and_time: Problem with reading in the time from the .xmf files.")
        raise

    return files_h5, files_xmf, time


def read_directory(postpath='.', verbose=True):
    """
    Creates a list of h5py File objects that correspond to each
    postprocessed HiFi simulation output file.  

    Sample usage
    ------------
    To read in a directory, run

        file_list, time = read_directory('.')

    To access data in the fourth output file, use

        file_list[3]["U01"][:,:]
    """

    assert isdir(expanduser(postpath)), \
        "read_directory: The input must be a directory."

    files_h5, files_xmf, time = find_files_and_time(postpath)

    assert len(files_h5) == len(files_xmf), \
        "Mismatch in number of HDF5 and xmf files in "+str(postpath)

    file_list = []
    for i in range(0,len(files_h5)):
        file = files_h5[i]
        f = h5py.File(file,'r')
        file_list.append(f)

    assert len(file_list) > 0, \
        "HDF5 files not found. Are you using the correct directory when calling read_directory?"
                
    return file_list, time


class hifi_class(object):
    """
    Reads in the list of h5py file objects that correspond to each
    postprocessed HiFi simulation output file and creates a class
    for all the postprocessed files in a simulation. This object
    contains all unnormalized HiFi variables and space-time axes

    Sample usage
    ------------
    To create a class from the files in adirectory, run

        data_set = hifi_class('/path/to/directory', 'simulation ID')

    To access a given axis or HiFi variable, use any of

        data_set.x
        data_set.y 
        data_set.time

        data_set.ni 
        data_set.Az 
        data_set.Bz 
        data_set.Vix
        data_set.Viy
        data_set.Viz
        data_set.Jz 
        data_set.pi 
        data_set.nn 
        data_set.Vnx
        data_set.Vny
        data_set.Vnz
        data_set.pn 

    To access the simulation ID, use

        data_set.name

    The default simulation ID is None
    """
    
    def __init__(self, postpath, simID=None):
        x, y, xx, yy = read_grid(postpath)
        file_list, time = read_directory(postpath)
        
        #axes for plotting
        self.x = xx
        self.y = yy
        self.time = time
        
        if simID is not None:
            self.name = simID
        else:
            self.name = 'no ID'
        
        U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13 =[
            np.empty((len(time),len(yy), len(xx))) for i in range(13)]
        
        for j in range(len(self.time)):
            U01[j,:,:] = file_list[j]['U01'][:,:]
            U02[j,:,:] = file_list[j]['U02'][:,:]
            U03[j,:,:] = file_list[j]['U03'][:,:]
            U04[j,:,:] = file_list[j]['U04'][:,:]
            U05[j,:,:] = file_list[j]['U05'][:,:]
            U06[j,:,:] = file_list[j]['U06'][:,:]
            U07[j,:,:] = file_list[j]['U07'][:,:]
            U08[j,:,:] = file_list[j]['U08'][:,:]
            U09[j,:,:] = file_list[j]['U09'][:,:]
            U10[j,:,:] = file_list[j]['U10'][:,:]
            U11[j,:,:] = file_list[j]['U11'][:,:]
            U12[j,:,:] = file_list[j]['U12'][:,:]
            U13[j,:,:] = file_list[j]['U13'][:,:]
        
        self.ni = U01
        self.Az = -U02
        self.Bz = U03
        self.Vix = np.divide(U04, U01)
        self.Viy = np.divide(U05, U01)
        self.Viz = np.divide(U06, U01)
        self.Jz = U07
        self.pi = U08
        self.nn = U09
        self.Vnx = np.divide(U10, U09)
        self.Vny = np.divide(U11, U09)
        self.Vnz = np.divide(U12, U09)
        self.pn = U13
