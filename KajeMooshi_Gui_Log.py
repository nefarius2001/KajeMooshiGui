import time, os, re
from datetime import datetime
import calendar
#import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import GetPaths
import Tkinter
from collections import deque

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

class Cdata:
	def __init__(self):
		self.dates = deque()
		self.x = deque()
		self.y_U = deque()
		self.y_I = deque()

def NewData_AppendDataset(new_timestamp,tmp_meas_A_kaje,tmp_meas_V_kaje,tmp_meas_Iraw,tmp_meas_Uraw):
	timestampnow=datetime.now()
	print "time Log: " + new_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	print "time now: " + timestampnow.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	print "A_kaje %.3f A "%tmp_meas_A_kaje
	print "V_Kaje %.3f V "%tmp_meas_V_kaje
	print "I_raw 0x%06X "%tmp_meas_Iraw
	print "I_raw 0x%06X "%tmp_meas_Uraw
	#print "delta xxx: " , delta.total_seconds()
	#timePlotStart=datetime.now()
	
	mydata.dates.append(new_timestamp)
	mydata.x.append(999) # to keep length persistant
	mydata.y_U.append(tmp_meas_V_kaje)
	mydata.y_I.append(tmp_meas_A_kaje)
	
	for k in range(0, len(mydata.dates)):
		mydata.x[k]=-((timestampnow - mydata.dates[k]).total_seconds())
		
	MAX_FALLBEHIND = -5
	if True:
		while(mydata.x[0] < MAX_FALLBEHIND):
			mydata.dates.popleft()
			mydata.x.popleft()
			mydata.y_U.popleft()
			mydata.y_I.popleft()
	
	line1.set_data(mydata.x ,mydata.y_U);
	line2.set_data(mydata.x ,mydata.y_I);
	lbl1_string.set("U = %.3f V"%tmp_meas_V_kaje)
	lbl2_string.set("I = %.3f A"%tmp_meas_A_kaje)
	
	for axFor in [ax1, ax2]:
		axFor.relim()
		axFor.set_xlim(MAX_FALLBEHIND, 0)
		axFor.autoscale(True,'y',True)
		#ax1.autoscale(True,'both',True)
	
def NewData_redraw():
	print "NewData_redraw"
	canvas1.draw()
	canvas2.draw()
	plt.draw()
	
	#ax1.show()
	#plt.pause(0.0001) #Note this correction
	#timePlotStop=datetime.now()
	#print "plotting took %.3f seconds"%((timePlotStop-timePlotStart).total_seconds())
def CheckLogForNewLine():
	where = logfile.tell()
	line = logfile.readline()
	iLines=0
	while(line):
		iLines=iLines+1
		print "new line"
		#print line, # already has newline
		#mo=re.search("this is line ([0-9]*)", line)
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
			# '%Y-%m-%d %H:%M:%S.%f'
			tmp_timestamp=datetime.strptime(tmp_timestamp_string, '%Y-%m-%d %H:%M:%S.%f')
			tmp_meas_A_kaje=float(mo.group(2))
			tmp_meas_V_kaje=float(mo.group(3))
			tmp_meas_Iraw  =float(mo.group(4))
			tmp_meas_Uraw  =float(mo.group(5))
			NewData_AppendDataset(tmp_timestamp,tmp_meas_A_kaje,tmp_meas_V_kaje,tmp_meas_Iraw,tmp_meas_Uraw)
		else:
			print "no RegEx match"
		print "next line"
		line = logfile.readline()
	if(iLines<=0):
		print "no line"
	else:
		print "there were %d lines" % iLines
		NewData_redraw()
def MainLoopCallback():
	print "MainLoopCallback: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	lbl3_string.set("time = "  + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
	CheckLogForNewLine()
	rootTk.after(100, MainLoopCallback)
startTime=0

TITLE_FONT="Helvetica 50 bold"
FIGURE_DPI=60

rootTk = Tkinter.Tk()

lbl1_string = Tkinter.StringVar()
label = Tkinter.Label( rootTk, textvariable=lbl1_string, font = TITLE_FONT, relief=Tkinter.RAISED )
lbl1_string.set("U = ????")
label.pack()

mydata=Cdata()
f1 = Figure(figsize=(5,5), dpi=FIGURE_DPI)
ax1 = f1.add_subplot(111)
line1, = ax1.plot([],[])
#line1 = Line2D(mydata.x,mydata.y, color='black')
#ax1.add_line(line1)

canvas1 = FigureCanvasTkAgg(f1, master = rootTk)
canvas1.show()
canvas1.get_tk_widget().pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas1, rootTk)
toolbar.update()
canvas1._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

lbl2_string = Tkinter.StringVar()
label = Tkinter.Label( rootTk, textvariable=lbl2_string, font = TITLE_FONT, relief=Tkinter.RAISED )
lbl2_string.set("I = ????")
label.pack()

f2 = Figure(figsize=(5,5), dpi=FIGURE_DPI)
ax2 = f2.add_subplot(111)
line2, = ax2.plot([],[])

canvas2 = FigureCanvasTkAgg(f2, master = rootTk)
canvas2.show()
canvas2.get_tk_widget().pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)

toolbar2 = NavigationToolbar2TkAgg(canvas2, rootTk)
toolbar2.update()
canvas2._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

lbl3_string = Tkinter.StringVar()
label = Tkinter.Label( rootTk, textvariable=lbl3_string, font = TITLE_FONT, relief=Tkinter.RAISED )
lbl3_string.set("time = ????")
label.pack()

button = Tkinter.Button(rootTk, text='Stop', width=25, command=rootTk.destroy)
button.pack()



rootTk.after(100, MainLoopCallback)
try:
	rootTk.mainloop()
except KeyboardInterrupt:
	print "quitting"
	pass
print "done"