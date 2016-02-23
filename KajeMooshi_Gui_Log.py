import time, os, re
from datetime import datetime
import calendar
#import numpy as np
import matplotlib.pyplot as plt
import GetPaths
import Tkinter

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

def NewLogLine_handler(tmp_meas_A_kaje,tmp_meas_V_kaje,tmp_meas_Iraw,tmp_meas_Uraw):
	if (startTime==0):
		startTime=tmp_timestamp
	print "time Log: ", tmp_timestamp
	print "time now: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	print "A_kaje %.3f A "%tmp_meas_A_kaje
	print "V_Kaje %.3f V "%tmp_meas_V_kaje
	print "I_raw 0x%06X "%tmp_meas_Iraw
	print "I_raw 0x%06X "%tmp_meas_Uraw
	delta=tmp_timestamp-startTime
	print "delta xxx: " , delta.total_seconds()
	timePlotStart=datetime.now()
	if not plt.fignum_exists((fig.number)):
		print "closed figure"
		plotDict=initPlot()
		fig=plotDict["fig"]
		ax1=plotDict["ax1"]
		ax2=plotDict["ax2"]
		
	ax1.scatter(delta.total_seconds() ,tmp_meas_V_kaje);
	ax2.scatter(delta.total_seconds() ,tmp_meas_A_kaje);
	
	#ax1.show()
	#plt.pause(0.0001) #Note this correction
	timePlotStop=datetime.now()
	print "plotting took %.3f seconds"%((timePlotStop-timePlotStart).total_seconds())
def CheckLogForNewLine():
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
		print "new line"
		#print line, # already has newline
		#mo=re.search("this is line ([0-9]*)", line)
		sRegex="([^;]*);" #time
		sRegex+=" AKaje=([\+\-0-9\.]*);"
		sRegex+=" VKaje=([\+\-0-9\.]*);"
		sRegex+=" Iraw=([\+\-0-9\.]*);"
		sRegex+=" Uraw=([\+\-0-9\.]*);"
		print sRegex
		mo=re.search(sRegex, line)
		if mo:
		#	print "match"		
			tmp_timestamp_string=mo.group(1)
			# '%Y-%m-%d %H:%M:%S.%f'
			tmp_timestamp=datetime.strptime(tmp_timestamp_string, '%Y-%m-%d %H:%M:%S.%f')
			tmp_meas_A_kaje=float(mo.group(2))
			tmp_meas_V_kaje=float(mo.group(3))
			tmp_meas_Iraw  =float(mo.group(4))
			tmp_meas_Uraw  =float(mo.group(5))
			NewLogLine_handler(tmp_meas_A_kaje,tmp_meas_V_kaje,tmp_meas_Iraw,tmp_meas_Uraw)
		else:
			print "no RegEx match"
def MainLoopCallback():
	print "MainLoopCallback: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	lbl1_string.set("Hey!? How are you doing?"  + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
	CheckLogForNewLine()
	rootTk.after(100, MainLoopCallback)
startTime=0

rootTk = Tkinter.Tk()
# Code to add widgets will go here...
rootTk.after(100, MainLoopCallback)

lbl1_string = Tkinter.StringVar()
label = Tkinter.Label( rootTk, textvariable=lbl1_string, font = "Helvetica 30 bold", relief=Tkinter.RAISED )
lbl1_string.set("Hey!? How are you doing?")
label.pack()
button = Tkinter.Button(rootTk, text='Stop', width=25, command=rootTk.destroy)
button.pack()
try:

	rootTk.mainloop()

except KeyboardInterrupt:
	print "quitting"
	pass
print "done"