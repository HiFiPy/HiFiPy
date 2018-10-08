# HiFiPy
Python software for analysis of HiFi simulations.  

## Installation

<!---
On Linux computers, if will often work to add the top-level directory
(the one containing the directory `hifipy' in lower case letters) to
your PYTHONPATH system variable.  Installation instructions on other
systems is not yet available.
--->
Build from source using the command

    python setup.py install

## Reading in 2D post-processed simulation output files
The following commands will allow access to the grid and the HDF5
files, and provide the time of each data file.

    import hifipy as hfp
    postpath = "/home/spacecat/HiFi_Runs/CaseA/post_out"
    x, y, xx, yy = hfp.read_grid(postpath)
    file_list, time = hfp.read_directory(postpath)

Then x and y will be 2D ndarrays with grid positions, and xx and yy
will be a 1D ndarray containing the grid positions if the x and y
positions are not functions of each other.  The time ndarray contains
the output times for each file, extracted from the xmf files.  The
file_list contains h5py File objects that allow access to the data.

To see the keys that are contained in each of the HDF5 files, use

    file_list[0].keys()

The first key will typically be "U01".  To get a slice of the "U01" in
the third output file, use 

    file_list[2]["U01"][:,0]

## Reading in 2D post-processed files as a class
The following commands will read in the grid and the HDF5 files and 
produce a class to contain the HiFi variables

    import hifipy as hfp
    postpath = "/home/spacecat/HiFi_Runs/CaseA/post_out"
    data_set = hfp.hifi_class(postpath)

To see grid or HiFi variable information, use

    data_set.x
 
 or
 
    data_set.ni 

All variables are as tracked by HiFi except for velocity, `data_set.vi[x/y/z]` 
or `data_set.vn[x/y/z]`, which is saved instead of momentum density

## Compatibility
This package should work in both Python 2.7 and 3.  

## License
HiFiPy is licensed under a three-clause BSD-style license contained in
the LICENSE.md file in the top-level directory.

## Contact information 
This package was created by Nick Murphy who can often be at
namurphy@cfa.harvard.edu.  Please contact Nick if you a user of HiFi
and would like to be given permission to continue development of this
package.

## Troubleshooting

### IOError on a Mac: `too many files'

On computers running Mac OS 10.10 and later, you may have to change
the system maximum number of open files to something greater than the
number of post-processed output files using the following commands:

    sudo launchctl limit maxfiles YOURLIMIT unlimited
    ulimit -n YOURLIMIT

Prior to OS 10.10, it should be sufficient to run:

    ulimit -n YOURLIMIT`

## Accessing HiFi
The HiFi website describes how to access the code:

    http://hifi-framework.webnode.com/hifi-framework/

