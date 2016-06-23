import time, os, re
from datetime import datetime
import calendar
import numpy as np
import matplotlib.pyplot as plt
import GetPaths

"""
KajeMooshiGui_plot_Log.py
This script plots the data from log file live
"""

#Set the filename and open the file
logfilename = GetPaths.GetMooshiLogFile_ForRead()
logfile = open(logfilename,'r')


#Find the size of the file and move to the end
st_results = os.stat(logfilename)
st_size = st_results[6]
logfile.seek(st_size)


def initPlot():
	# init plot
	plt.ion() ## Note this correction
	fig_local, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	#myFigNum=fig.number
	#plt.axis([0,1000,0,1])
	ax1.set_xlabel('time [s]')
	ax1.set_ylabel('voltage [V]')
	ax2.set_xlabel('time [s]')
	ax2.set_ylabel('current [A]')
	#print "figure is ", fig
	return {'fig':fig_local, 'ax1':ax1 ,'ax2':ax2 }

plotDict=initPlot()
fig=plotDict["fig"]
ax1=plotDict["ax1"]
ax2=plotDict["ax2"]
xlist_T=list();
ylist_U=list();
ylist_I=list();

startTime=0

try:
	while 1:
		where = logfile.tell()
		line = logfile.readline()
		if not line:
			timeStart=datetime.now()
			time.sleep(0.001)
			plt.pause(0.0001) #Note this correction
			logfile.seek(where)
			timeStop=datetime.now()
			#print "no line, paused %.3f seconds"%((timeStop-timeStart).total_seconds())
		else:
			print ""
			print "new line"
			#print line, # already has newline
			sRegex="([^;]*);" #time
			sRegex+=" AKaje=([\+\-0-9\.]*);"
			sRegex+=" VKaje=([\+\-0-9\.]*);"
			sRegex+=" Iraw=([\+\-0-9\.]*);"
			sRegex+=" Uraw=([\+\-0-9\.]*);"
			#print sRegex
			mo=re.search(sRegex, line)
			if mo:
			#	print "match"		
				tmp_timestamp_string=mo.group(1)
				tmp_timestamp  =datetime.strptime(tmp_timestamp_string, '%Y-%m-%d %H:%M:%S.%f')
				tmp_meas_A_kaje=float(mo.group(2))
				tmp_meas_V_kaje=float(mo.group(3))
				tmp_meas_Iraw  =float(mo.group(4))
				tmp_meas_Uraw  =float(mo.group(5))
				if (startTime==0):
					startTime=tmp_timestamp
				delta=tmp_timestamp-startTime
				
				print "time Log: ", tmp_timestamp
				print "time now: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
				print "delta xxx: " , delta.total_seconds()
				print "I_raw 0x%06X "%tmp_meas_Iraw
				print "U_raw 0x%06X "%tmp_meas_Uraw
				print "A_kaje %.3f A "%tmp_meas_A_kaje
				print "V_Kaje %.3f V "%tmp_meas_V_kaje
				
				timePlotStart=datetime.now()
				if not plt.fignum_exists((fig.number)):
					print "closed figure"
					plotDict=initPlot()
					fig=plotDict["fig"]
					ax1=plotDict["ax1"]
					ax2=plotDict["ax2"]
				
				xlist_T.append(delta.total_seconds());
				ylist_U.append(tmp_meas_V_kaje);
				ylist_I.append(tmp_meas_A_kaje);
				while(len(xlist_T)>30):
					xlist_T.pop(0)
					ylist_U.pop(0)
					ylist_I.pop(0)
				xarray_T = np.array(xlist_T);
				yarray_U = np.array(ylist_U);
				yarray_I = np.array(ylist_I);
				ax1.clear()
				ax2.clear()
				#ax1.scatter(delta.total_seconds() ,tmp_meas_V_kaje);
				ax1.scatter(xarray_T,yarray_U);
				ax2.scatter(xarray_T,yarray_I);
				ax1.set_title("U = %.3f V"%tmp_meas_V_kaje)
				ax2.set_title("I = %.3f A"%tmp_meas_A_kaje)
				
				#ax1.show()
				#plt.pause(0.0001) #Note this correction
				timePlotStop=datetime.now()
				print "plotting took %.3f seconds"%((timePlotStop-timePlotStart).total_seconds())
			else:
				print "no RegEx match"

except KeyboardInterrupt:
	print "quitting"
	quit()