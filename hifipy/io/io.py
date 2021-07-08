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

    >>> import hifipy as hfp
    >>> postpath = "~/HiFi_Runs/20161020a_LaminarBaseRun_LoRes/post_out_4_4"
    >>> x, y, xx, yy = hfp.read_grid(postpath)
    >>> file_list, time = hfp.read_directory(postpath)

To see the keys that are contained in each of the HDF5 files, use

    >>> file_list[0].keys()

The first key will typically be "U01".  To get a slice of the "U01" in
the third output file, use

    >>> file_list[2]["U01"][:,0]

"""

import glob
import numpy as np
import h5py

from os.path import expanduser, isdir, isfile
from typing import Optional, List

def read_grid(postpath: str = '.'):
    """
    Reads in grid information from a HiFi simulation.

    Inputs
    ------
    The sole input, postpath, must be a directory that contains the
    output files from a HiFi simulation, including a grid file such as
    grid_00000.h5.

    Sample usage
    ------------
    >>> x, y, xx, yy = hifipy.read_grid('~/HiFi_Runs/20161020a_LaminarBaseRun_LoRes')

    """

    if not isdir(expanduser(postpath)):
        raise IOError("The input to read_grid must be a directory.")

    files_grid = glob.glob(postpath+'/grid*.h5')

    if len(files_grid) <= 0:
        raise IOError("Grid file not found.")

    files_grid.sort()

    gridfile = files_grid[0]
    grid = h5py.File(gridfile,'r')

    x_2D, y_2D = np.array(grid['U01']), np.array(grid['U02'])
    x_1D, y_1D = np.array(x_2D[0,:]), np.array(y_2D[:,0])

    return x_2D, y_2D, x_1D, y_1D


def find_files_and_time(postpath: str = '.'):
    """
    Creates a list of the HDF5 and xmf files in a directory, and reads
    in the time from the xmf files into an array.

    Sample usage
    ------------
    >>> files_h5, files_xmf, time = find_files_and_time('.')

    Notes
    -----
    The time calculation is sensitive to the format of the xmf files.
    If that format changes, then this routine will have to be
    modified.
    """
    if not isdir(expanduser(postpath)):
        raise IOError("The input to find_files_and_time must be a directory.")

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
    except Exception:
        raise IOError("Unable to read in the time from .xmf files.")

    return files_h5, files_xmf, time


def read_directory(postpath: str ='.'):
    """
    Creates a list of ``h5py`` `File` instances that correspond to each
    postprocessed HiFi simulation output file.

    Sample usage
    ------------
    To read in a directory, run

        >>> file_list, time = read_directory('.')

    To access data in the fourth output file, use

        >>> file_list[3]["U01"][:,:]

    """

    if not isdir(expanduser(postpath)):
        raise IOError("The input to read_directory must be a directory.")

    files_h5, files_xmf, time = find_files_and_time(postpath)

    if len(files_h5) != len(files_xmf):
        raise IOError("Mismatch in number of HDF5 and XMF files.")

    file_list = []
    for i in range(0,len(files_h5)):
        file = files_h5[i]
        f = h5py.File(file,'r')
        file_list.append(f)

    if len(file_list) < 1:
        raise IOError(f"No HDF5 files are found in {postpath}.")

    return file_list, time


class hifi_class:
    """
    Reads in the list of ``h5py`` `File` objects that correspond to each
    postprocessed HiFi simulation output file and creates a class
    for all the postprocessed files in a simulation. This object
    contains all unnormalized HiFi variables and space-time axes.

    Sample usage
    ------------
    To create a class from the files in a directory, run

        >>> data_set = hifi_class('/path/to/directory', 'simulation ID')

    To access a given axis or HiFi variable, use any of

        >>> data_set.x
        >>> data_set.y
        >>> data_set.time
        >>> data_set.ni
        >>> data_set.Az
        >>> data_set.Bz
        >>> data_set.Vix
        >>> data_set.Viy
        >>> data_set.Viz
        >>> data_set.Jz
        >>> data_set.pp
        >>> data_set.nn
        >>> data_set.Vnx
        >>> data_set.Vny
        >>> data_set.Vnz
        >>> data_set.pn

    To access the simulation ID, use

        >>> data_set.name

    The default simulation ID is None.
    """

    def _get_grid(self):
        x, y, xx, yy = read_grid(self.postpath)
        self._data['x'] = xx
        self._data['y'] = yy

    def _get_file_list_and_time(self):
        try:
            file_list, time = read_directory(self.postpath)
        except Exception as exc:
            raise IOError(f"Unable to read in HDF5 files in {postpath}") from exc

        self._data['file_list'] = file_list
        self._data['time'] = time

    def _assign_variables_to__data_dict(self):
        nt, nx, ny = len(self.time), len(self.x), len(self.y)

        U01_through_U13 = [f"U{'0' if n < 10 else ''}{n}" for n in range(1, 14)]

        simulation_results = {
            variable: np.empty([nt, ny, nx])
            for variable in U01_through_U13
        }

        print(self.file_list)

        for variable in U01_through_U13:
            for time_index in range(nt):
                simulation_results[variable][time_index, :, :] = \
                    self.file_list[time_index][variable][:, :]

        try:
            self._data['ni'] = simulation_results['U01']
            self._data['Az'] = -simulation_results['U02']
            self._data['Bz'] = simulation_results['U03']
            self._data['Vix'] = np.divide(simulation_results['U04'], simulation_results['U01'])
            self._data['Viy'] = np.divide(simulation_results['U05'], simulation_results['U01'])
            self._data['Viz'] = np.divide(simulation_results['U06'], simulation_results['U01'])
            self._data['Jz'] = simulation_results['U07']
            self._data['pp'] = simulation_results['U08']
            self._data['nn'] = simulation_results['U09']
            self._data['Vnx'] = np.divide(simulation_results['U10'], simulation_results['U01'])
            self._data['Vny'] = np.divide(simulation_results['U11'], simulation_results['U01'])
            self._data['Vnz'] = np.divide(simulation_results['U12'], simulation_results['U01'])
            self._data['pn'] = simulation_results['U13']
        except Exception as exc:
            raise Exception("Unable to create _data private attribute.") from exc

    def _B_from_Az(self):
        self._data['Bx'] = np.empty_like(self.Az)
        self._data['By'] = np.empty_like(self.Az)
        for time_index in range(len(self.time)):
            gradient_of_Az = np.gradient(self.Az[time_index, :, :], self.y, self.x, edge_order=2)
            self._data['Bx'][time_index,:,:] = gradient_of_Az[0]
            self._data['By'][time_index,:,:] = gradient_of_Az[1]

    def __init__(self, postpath: str = '.', simID: Optional[str] = None):
        if simID is not None and not isinstance(simID, str):
            raise TypeError("simID must be a string or None.")

        self._data = {}
        self.name = simID
        self.postpath = postpath

        self._get_grid()
        self._get_file_list_and_time()
        self._assign_variables_to__data_dict()
        self._B_from_Az()

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    @name.setter
    def name(self, simID):
        self._data['name'] = simID if simID is not None else "no ID"

    @property
    def file_list(self) -> List:
        return self._data['file_list']

    @property
    def postpath(self) -> str:
        return self._data['postpath']

    @postpath.setter
    def postpath(self, path_to_postprocessed_files: str):
        if not isinstance(path_to_postprocessed_files, str):
            raise TypeError("Need a string.")
        if not isdir(expanduser(path_to_postprocessed_files)):
            raise ValueError(f"Need a directory.")
        self._data['postpath'] = path_to_postprocessed_files

    @property
    def x(self) -> np.ndarray:
        return self._data['x']

    @property
    def y(self) -> np.ndarray:
        return self._data['y']

    @property
    def time(self) -> np.ndarray:
        return self._data['time']

    @property
    def ni(self) -> np.ndarray:
        return self._data['ni']

    @property
    def Az(self) -> np.ndarray:
        return self._data['Az']

    @property
    def Bz(self) -> np.ndarray:
        return self._data['Bz']

    @property
    def Vix(self) -> np.ndarray:
        return self._data['Vix']

    @property
    def Viy(self) -> np.ndarray:
        return self._data['Viy']

    @property
    def Viz(self) -> np.ndarray:
        return self._data['Viz']

    @property
    def Jz(self) -> np.ndarray:
        return self._data['Jz']

    @property
    def pp(self) -> np.ndarray:
        return self._data['pp']

    @property
    def nn(self) -> np.ndarray:
        return self._data['nn']

    @property
    def Vnx(self) -> np.ndarray:
        return self._data['Vnx']

    @property
    def Vny(self) -> np.ndarray:
        return self._data['Vny']

    @property
    def Vnz(self) -> np.ndarray:
        return self._data['Vnz']

    @property
    def pn(self) -> np.ndarray:
        return self._data['pn']

    @property
    def Bx(self) -> np.ndarray:
        return self._data['Bx']

    @property
    def By(self) -> np.ndarray:
        return self._data['By']

    @property
    def Nx(self) -> int:
        return len(self.x)

    @property
    def Ny(self) -> int:
        return len(self.y)

    @property
    def Nt(self) -> int:
        return len(self.time)