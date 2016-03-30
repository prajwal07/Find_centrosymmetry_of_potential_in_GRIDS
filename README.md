# Find_centrosymmetry_of_potential_in_GRIDS
Python Script to estimate centrosymmetry of potential in Debye–Hückel potential sphere in GRID files
#################################################################
####################### DESCRIPTION #############################
#################################################################

Python Script to estimate centrosymmetry of potential in Debye–Hückel potential sphere in GRID files.

By: Prajwal Nandekar
Email: prajwal.pharm07@gmail.com
Updated on: 21st March 2016

Command:
python centrosymmetry_potential.py -i grid_filename.grd

It requires Input file for Electrostatics Potential grid in UHBD format.
(Example: protein.grd).

Requirements:

Python: Scientific Python packages

Required modules
########################
import sys,os
import itertools
from scipy import stats
import numpy as np
import argparse
#######################

Application:

Python Script to Estimate centrosymmetry of potential.

Description:

This script estimates the asymmetry in the potential field. Prior to running this script 
an electrostatic calculation should be done at a large enough grid spacing to ensure that the
potential will become centrosymmetric before the edge of the grid.

Sample Input files:
From tutorial: Calculation of electrostatic potentials with UHBD
Weblink: http://projects.h-its.org/mcm/projects/afwb-2002/uhbd.html

        :Arguments:
            *gridfile*
		Input file for Electrostatics Potential grid in UHBD format. (Example: protein_uhbd.grd).
        
        :Returns:
            *AVERAGED POTENTIALS ALONG GIRD DIMENSIONS FROM CENTER OF GRID*

Command:
        python centrosymmetry_potential.py -i grid_filename.grd

#################################################################
########################### E N D ###############################
#################################################################
