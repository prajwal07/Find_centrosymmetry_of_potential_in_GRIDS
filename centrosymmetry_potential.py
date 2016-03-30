#!/sw/mcm/app/anaconda/2.3.0/envs/mdaenv/bin/python
import sys,os
import itertools
from scipy import stats
import numpy as np
import argparse

######################################################

parser = argparse.ArgumentParser(description='\n Estimate centrosymmetry of potential. \n "Command:" \n "python centrosymmetry_potential.py -i grid_filename.grd" ')
parser.add_argument('-i', '--input', dest = "gridfile", help='Input File name of Electrostatics Potential grid in UHBD format (Example: protein_uhbd.grd).')
args = parser.parse_args()

#####################################################
"""
Application:

Python Script to Estimate centrosymmetry of potential.

Description:

This script estimates the asymmetry in the potential field. Prior to running this script
an electrostatic calculation should be done at a large enough grid spacing to ensure that the
potential will become centrosymmetric before the edge of the grid.

        :Arguments:
            *gridfile*
                Input file for Electrostatics Potential grid in UHBD format. (Example: protein.grd).

        :Returns:
            *AVERAGED POTENTIALS ALONG GIRD DIMENSIONS FROM CENTER OF GRID*

Command:
        python centrosymmetry_potential.py -i grid_filename.grd
"""
#####################################################

PATH = os.getcwd()
print '\nCurrent working directory is:', PATH
print ""
############### INPUT and TEMP OUTPUT FILES AND FILENAMES ##############

input_file_name = args.gridfile
input_file = open(input_file_name,"r")
input_file_lines = input_file.readlines()
input_file.close()

output_file_name_Z = "output_Z"
output_file_lines_Z = []
output_Z = "central_index" + " " + "plane_number" + " " + "total_p_values" + " " + "central_value_zaxis_plane" + "\n"

output_file_name_Y = "output_Y"
output_file_lines_Y = []
output_Y = "central_index" + " " + "plane_number" + " " + "total_p_values" + " " + "central_value_yaxis_plane" + "\n"

output_file_name_X = "output_X"
output_file_lines_X = []
output_X = "central_index" + " " + "plane_number" + " " + "total_p_values" + " " + "central_value_xaxis_plane" + "\n"

############### READING GRID FILE ######################

######## GET GRID POINTS AND GRID PLANES DATA ##########
with open(input_file_name) as f:
    for line in itertools.islice(f, 2, 3):  # start=2 (3rd line), stop=3 (4th line), This the line contains GRID DIMENSIONS
	split_line=line.split()
	xdim = int(split_line[0]) # X-dimension
	ydim = int(split_line[1]) # Y-dimension
	zdim = int(split_line[2]) # Z-dimension
	grid_dim_line = ('%4d' % xdim) + ('%4d' % ydim) + ('%4d' % zdim) + "\n"
	grid_points_one_plane = xdim*ydim
	number_of_planes = zdim
	total_grid_points = xdim*ydim*zdim

print "###############################################################"
print "                 GRID DIMENSIONS AND STATS"
print "###############################################################"
print ""
print "Dimension of GRID is %4d  X %4d  X %4d" % (xdim, ydim, zdim)
print "Total number of grid points in GRID BOX = ", int (xdim*ydim*zdim)
lines_in_one_plane = int ((grid_points_one_plane/6)+1)
print "Number of line in One Plane (input GRIDFILE) = ", lines_in_one_plane
print "Number of grid points in one plane =", grid_points_one_plane
print "Number of planes = ", number_of_planes
print ""
print "###############################################################"

############### READ GRID POINTS ###############################

################ FOR Z-AXIS DIRECTION VALUES ##############################
def read_grids_zaxis(plane):

    # For plane number 1 to 65, IF Grid size is 65 x 65 x 65

    grid_dim_line = "   " + ('%4d' % plane_number) + "   " + ('%4d' % ydim) + "   " + ('%4d' % zdim) + "\n" #   1    65   65
    plane_number_next = plane_number + 1
    next_plane = "   " + ('%4d' % plane_number_next) + "   " + ('%4d' % ydim) + "   " + ('%4d' % zdim) + "\n" #   2    65   65
    flag=0
    array_zaxis = []
    for line_num, line in enumerate(input_file_lines, 1):
        if grid_dim_line in line:
            flag=1
        elif next_plane in line:
            break
        elif (flag==1):
            for word in line.strip().split():
                array_zaxis.append(float(word))

    total_p_values = len(array_zaxis) # 4225
    central_index = ((xdim*ydim)/2)  # 2112
    central_value_zaxis_plane = array_zaxis[central_index]
    actual_index = central_index + 1
#    print "Central value along Z-axis is %f and have index of %d for plane number %d (Total potential values %d)" % (central_value_zaxis_plane, actual_index, plane_number, total_p_values)
    output_Z = ('%d' % actual_index) + " " + ('%d' % plane_number) + " " + ('%d' % total_p_values) + " " + ('%f' % central_value_zaxis_plane) + "\n"
    output_file_lines_Z.append(output_Z) # WRITE in temp output file
  

################ FOR X-AXIS DIRECTION VALUES ##############################
def read_grids_xaxis(plane_number):

    # For plane number 33
    grid_dim_line = "   " + ('%4d' % plane_number) + "   " + ('%4d' % ydim) + "   " + ('%4d' % zdim) + "\n"    #   33    65   65
    plane_number_next = plane_number + 1
    next_plane = "   " + ('%4d' % plane_number_next) + "   " + ('%4d' % ydim) + "   " + ('%4d' % zdim) + "\n"    #   34    65   65
    flag=0
    array_xaxis = []
    for line_num, line in enumerate(input_file_lines, 1):
        if grid_dim_line in line:
            flag=1
        elif next_plane in line:
            break
        elif (flag==1):
            for word in line.strip().split():
                array_xaxis.append(float(word))
    line_count= 0
    total_p_values = len(array_xaxis)
    start_index = (xdim * int (ydim/2))
    last_index = int (start_index + xdim)
    for i in range (start_index, last_index): # (2080, 2145))
        central_index = ((xdim*ydim)/2)
        central_value_xaxis_plane = array_xaxis[i]
        actual_index = i + 1
	line_count = line_count + 1
#        print "Central value along X-axis is %f and have index of %d for plane number %d (Total potential values %d)" % (central_value_xaxis_plane, actual_index, plane_number, total_p_values)
        output_X = ('%d' % actual_index) + " " + ('%d' % line_count) + " " + ('%d' % total_p_values) + " " + ('%f' % central_value_xaxis_plane) + "\n"
        output_file_lines_X.append(output_X) # WRITE in temp output file

################ FOR Y-AXIS DIRECTION VALUES ##############################

def read_grids_yaxis(plane_number):

    # For plane number 33
    grid_dim_line = "   " + ('%4d' % plane_number) + "   " + ('%4d' % ydim) + "   " + ('%4d' % zdim) + "\n"   #   33    65   65
    plane_number_next = plane_number + 1
    next_plane = "   " + ('%4d' % plane_number_next) + "   " + ('%4d' % ydim) + "   " + ('%4d' % zdim) + "\n"   #   34    65   65
    flag=0
    array_yaxis = []
    for line_num, line in enumerate(input_file_lines, 1):
        if grid_dim_line in line:
            flag=1
        elif next_plane in line:
            break
        elif (flag==1):
            for word in line.strip().split():
                array_yaxis.append(float(word))

    total_p_values = len(array_yaxis)
    start_index = int (xdim/2)
    last_index = total_p_values
    line_count= 0

    for i in range (start_index, last_index, ydim):  # (32, 4225, 65)
	line_count = line_count + 1
        central_value_yaxis_plane = array_yaxis[i]
        actual_index = i + 1
#        print "Central value along Y-axis is %f and have index of %d for plane number %d (Total potential values %d)" % (central_value_yaxis_plane, actual_index, plane_number, total_p_values)
        output_Y = ('%d' % actual_index) + " " + ('%d' % line_count) + " " + ('%d' % total_p_values) + " " + ('%f' % central_value_yaxis_plane) + "\n"
        output_file_lines_Y.append(output_Y) # WRITE in temp output file

################ RUN THE FUNCTIONS ####################################

for plane in range(0, number_of_planes): # FOR Potential grid values in Z direction
    plane_number = plane + 1
    read_grids_zaxis(plane)

for plane in range(0, number_of_planes):
    plane_number = plane + 1
    line_count = 0
    if (plane_number==(int (zdim/2)+1)): # FOR Potential grid values in X and Y direction
	read_grids_xaxis(plane_number)
        read_grids_yaxis(plane_number)

#########################################################################
output_file_X = open(output_file_name_X, 'w')
output_file_X.writelines(output_file_lines_X)

output_file_Y = open(output_file_name_Y, 'w')
output_file_Y.writelines(output_file_lines_Y)

output_file_Z = open(output_file_name_Z, 'w')
output_file_Z.writelines(output_file_lines_Z)

########################################################################################################
#################### DATA PROCESSING ###################################################################
########################################################################################################

output_file_X = open(output_file_name_X, 'r')
output_file_Y = open(output_file_name_Y, 'r')
output_file_Z = open(output_file_name_Z, 'r')

################ READING THE TEMP OUTPUT FILES ####################
input_file_lines_X = output_file_X.readlines()
input_file_lines_Y = output_file_Y.readlines()
input_file_lines_Z = output_file_Z.readlines()

array_xaxis = []
array_yaxis = []
array_zaxis = []

for linex in input_file_lines_X:
    array_xaxis.append(linex.strip().split())
for liney in input_file_lines_Y:
    array_yaxis.append(liney.strip().split())
for linez in input_file_lines_Z:
    array_zaxis.append(linez.strip().split())

center_index = int (ydim/2) # Index for Center of GRID
center_x = array_xaxis[center_index][3]  # 4th column is for Potential values
center_y = array_yaxis[center_index][3]  # 4th column is for Potential values
center_z = array_zaxis[center_index][3]  # 4th column is for Potential values

center_average = (float(center_x) + float(center_y) + float(center_z))/3 

i = 0 
# VAriable to count distance in Angstrom from from CENTER point of grid

print ""
print "PRINT MODULE"
print "PRINTING AVERAGED POTENTIALS ALONG GIRD DIMENSIONS FROM CENTER OF GRID: \n"
print "Distance(A) Along X-axis  X'-axis      Y-axis     Y'-axis     Z-axis      Z'-axis  Average Pot. \n"
print "    " + ('%-3d' % i) + "A  " + ('%12.6f' % float(center_x)) + ('%12.6f' % float(center_x)) + ('%12.6f' % float(center_y)) + ('%12.6f' % float(center_y)) + ('%12.6f' % float(center_z)) + ('%12.6f' % float(center_z)) + ('%12.6f' % float(center_average))

for j in range (1, center_index+1):
    positive = (center_index + j) # index for reading values in positive direction from CENTER point
    negative = (center_index - j) # index for reading values in Negative direction from CENTER point
    positive_x = array_xaxis[positive][3]
    positive_y = array_yaxis[positive][3]
    positive_z = array_zaxis[positive][3]
    negative_x = array_xaxis[negative][3]
    negative_y = array_yaxis[negative][3]
    negative_z = array_zaxis[negative][3]
    i = j
    average = (float (positive_x) + float (negative_x) + float (positive_y) + float (negative_y) + float (positive_z) + float (negative_z))/6  # Calculate avrage of All 6 points

    print "    " + ('%-3d' % i) + "A  " + ('%12.6f' % float(positive_x)) + ('%12.6f' % float(negative_x)) + ('%12.6f' % float(positive_y)) + ('%12.6f' % float(negative_y)) + ('%12.6f' % float(positive_z)) + ('%12.6f' % float(negative_z)) + ('%12.6f' % float(average))

############################ CLOSE AND REMOVE INTERMEDIATE TEMP FILES ##################################
output_file_X.close()
output_file_Y.close()
output_file_Z.close()

os.remove("output_X")
os.remove("output_Y")
os.remove("output_Z")

