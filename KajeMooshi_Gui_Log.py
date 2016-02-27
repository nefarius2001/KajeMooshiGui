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
        self.x = []
        self.y = []

def NewLogLine_handler(tmp_timestamp,tmp_meas_A_kaje,tmp_meas_V_kaje,tmp_meas_Iraw,tmp_meas_Uraw):
	print "time Log: " + tmp_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	print "time now: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	print "A_kaje %.3f A "%tmp_meas_A_kaje
	print "V_Kaje %.3f V "%tmp_meas_V_kaje
	print "I_raw 0x%06X "%tmp_meas_Iraw
	print "I_raw 0x%06X "%tmp_meas_Uraw
	#print "delta xxx: " , delta.total_seconds()
	#timePlotStart=datetime.now()
	
	data1.x.append(len(data1.y)+1)
	data1.y.append(tmp_meas_V_kaje)
	data2.x.append(len(data2.y)+1)
	data2.y.append(len(data2.y)+1)
	
	line1.set_data(data1.x ,data1.y);
	l2.set_data(data2.x ,data2.y);
	lbl1_string.set("U = %.3f V"%tmp_meas_V_kaje)
	lbl2_string.set("I = %.3f A"%tmp_meas_A_kaje)
	
	ax1.relim()
	ax1.autoscale(True,'both',True)
	ax2.relim()
	ax2.autoscale(True,'both',True)
	
	
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
	if not line:
		print "no line"
	else:
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
			NewLogLine_handler(tmp_timestamp,tmp_meas_A_kaje,tmp_meas_V_kaje,tmp_meas_Iraw,tmp_meas_Uraw)
		else:
			print "no RegEx match"
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

data1=Cdata()
data1.x=[1,2,3,4]
data1.y=[0.1,0,-0.1,0]
f1 = Figure(figsize=(5,5), dpi=FIGURE_DPI)
ax1 = f1.add_subplot(111)
line1, = ax1.plot(data1.x,data1.y)
#line1 = Line2D(data1.x,data1.y, color='black')
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

data2=Cdata()
data2.x=[1,2,3,4]
data2.y=[1,2,3,4]
f2 = Figure(figsize=(5,5), dpi=FIGURE_DPI)
ax2 = f2.add_subplot(111)
l2, = ax2.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

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