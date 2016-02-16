import time, os
from datetime import datetime
# numpy for random
import numpy as np 

import GetPaths

"""
Mooshi_to_Log_dummy.py
This script provides random data to develop/debug the plotting gui
"""

#Set the filename and open the file
logfilename = GetPaths.GetMooshiLogFile_ForWrite()
print logfilename
logfile = open(logfilename,'w')

iLine=0
while 1:
	iLine+=1
	sTime=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	tmp_meas_A_kaje=np.random.random();
	tmp_meas_V_kaje=np.random.random();
	tmp_meas_Iraw=9999*np.random.random();
	tmp_meas_Uraw=9999*np.random.random();
	
	sTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	sLine=sTime + "; AKaje=%.6f;"%tmp_meas_A_kaje + " VKaje=%.6f;"%tmp_meas_V_kaje + " Iraw=%08i;"%tmp_meas_Iraw  + " Uraw=%08i;"%tmp_meas_Uraw 
	print sLine
	logfile.write(sLine + "\n")
	logfile.flush()
	
	time.sleep(0.1)