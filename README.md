# HiFiPy
Python software for analysis of HiFi simulations

## Reading in 2D post-processed simulation output files
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