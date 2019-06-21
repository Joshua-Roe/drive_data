#! /usr/bin/env python

import csv
from os import path

# output format
# wz, ax, wz, vx, Il, IR

## uses hard coded file names, files are to be placed within the csv folder in the package directory
basepath = path.dirname(__file__)
imuFile = path.abspath(path.join(basepath, "..", "csv/imu.csv"))
velFile = path.abspath(path.join(basepath, "..", "csv/vel.csv"))
statusFile = path.abspath(path.join(basepath, "..", "csv/status.csv"))
outFile = path.abspath(path.join(basepath, "..", "csv/output_fill_blanks.csv"))

#IMU want colum 0, 24, 35 as of second line (due to multivalue cells)
with open(imuFile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header = next(reader)
    print(header)
    csvfile.seek(0)
    h = sum(1 for row in reader)
    w = sum(1 for col in header)
    print("IMU",h,w)
    nImu = h
    imu = [[0 for x in range(w)] for y in range(h)]
    curRow = 0
    csvfile.seek(0)
    for row in reader:
        ##print(row[0])
        if row[1] == "header": continue
        imu[curRow][0] = row[0]
        imu[curRow][1] = row[24]
        imu[curRow][2] = row[35]
        curRow = curRow + 1

#vel want colums 0, 2, 8
with open(velFile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header = next(reader)
    print(header)
    csvfile.seek(0)
    h = sum(1 for row in reader)
    w = sum(1 for col in header)
    print("Vel",h,w)
    nVel = h
    vel = [[0 for x in range(w)] for y in range(h)]
    curRow = 0
    csvfile.seek(0)
    for row in reader:

        ##print(row[0])
        vel[curRow][0] = row[0]
        vel[curRow][1] = row[2]
        vel[curRow][2] = row[8]
        curRow = curRow + 1

#status want colums 0, 10, 11
with open(statusFile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header = next(reader)
    print(header)
    csvfile.seek(0)
    h = sum(1 for row in reader)
    w = sum(1 for col in header)
    print("status",h,w)
    nStatus = h
    status = [[0 for x in range(w)] for y in range(h)]
    curRow = 0
    csvfile.seek(0)
    for row in reader:
        #print(row[0])
        #print(row[11])
        status[curRow][0] = row[0]
        status[curRow][1] = row[10]
        status[curRow][2] = row[11]
        curRow = curRow + 1

with open(outFile, 'w') as csvfilefinal:
    writer = csv.writer(csvfilefinal, delimiter=',', quotechar='|')
    iImu = 2
    iVel = 2
    iStatus = 2

    print('----------')
    print('Converting')
    #wz, ax, vx, wz, Il, IR
    ##exit()
    writer.writerow(['ROS Timestamp', 'IMU Z rotation', 'IMU X acceleration', 'cmd_vel X translation', 'cmd_vel Z rotation', 'left motor current', 'right motor current'])
    while iImu < nImu and iVel < nVel and iStatus < nStatus:
        if iVel == nVel and iStatus == nStatus:
            writer.writerow([imu[iImu][0], imu[iImu][1], imu[iImu][2], vel[iVel-1][1], vel[iVel-1][2], status[iStatus-1][1], status[iStatus-1][2]])
            ##print('imu')
            iImu = iImu + 1
        elif iImu == nImu and iStatus == nStatus:
            writer.writerow([vel[iVel][0], imu[iImu-1][1], imu[iImu-1][2], vel[iVel][1], vel[iVel][2],status[iStatus-1][1], status[iStatus-1][2]])
            ##print('vel')
            iVel = iVel + 1
        elif iImu == nImu and iVel == nVel:
            writer.writerow([status[iStatus][0], imu[iImu-1][1], imu[iImu-1][2], vel[iVel-1][1], vel[iVel-1][2], status[iStatus][1], status[iStatus][2]])
            ##print('status')
            iStatus = iStatus + 1
        elif float(imu[iImu][0]) <= float(vel[iVel][0]) and float(imu[iImu][0]) <= float(status[iStatus][0]):
            writer.writerow([imu[iImu][0], imu[iImu][1], imu[iImu][2], vel[iVel-1][1], vel[iVel-1][2], status[iStatus-1][1], status[iStatus-1][2]])
            ##print('imusort')
            iImu = iImu + 1
        elif float(vel[iVel][0]) <= float(imu[iImu][0]) and float(vel[iVel][0]) <= float(status[iStatus][0]):
            writer.writerow([vel[iVel][0], imu[iImu-1][1], imu[iImu-1][2], vel[iVel][1], vel[iVel][2], status[iStatus-1][1], status[iStatus-1][2]])
            ##print('velsort')
            iVel = iVel + 1
        elif float(status[iStatus][0]) <= float(imu[iImu][0]) or float(status[iStatus][0]) <= float(vel[iVel][0]):
            writer.writerow([status[iStatus][0], imu[iImu-1][1], imu[iImu-1][2], vel[iVel-1][1], vel[iVel-1][2], status[iStatus][1], status[iStatus][2]])
            ##print('statussort')
            iStatus = iStatus + 1
        else:
            print("broken")
            exit()
print('Conversion Complete')