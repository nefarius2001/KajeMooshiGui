from MooshimeterAPI import BGWrapper
from MooshimeterAPI.Mooshimeter import Mooshimeter

from operator import attrgetter

from datetime import datetime
import GetPaths


#Set the filename and open the file
logfilename = GetPaths.GetMooshiLogFile_ForWrite()
logfile = open(logfilename,'w')


"""
Mooshi_to_Log.py
This script handles the connection to the Mooshimeter logs it to a file.
It stems from the Example.py and does the following:
- Scan for BLE devices
- Filter for Mooshimeters
- Connect to the Mooshimeter with strongest signal
- Configure the meter to read Voltage in 60V range and Current in 10A range
- Begin streaming data to log file (and printing the results to the console)
"""

if __name__=="__main__":
	# Set up the lower level to talk to a BLED112 in port COM4
	# REPLACE THIS WITH THE BLED112 PORT ON YOUR SYSTEM
	BGWrapper.initialize("COM4")
	# Scan for 3 seconds
	scan_results = BGWrapper.scan(3)
	# Filter for devices advertising the Mooshimeter service
	meters = filter(lambda(p):Mooshimeter.mUUID.METER_SERVICE in p.ad_services, scan_results)
	if len(meters) == 0:
		print "No Mooshimeters found"
		exit(0)
	# Display detected meters
	for m in meters:
		print m
	def connectToMeterAndStream(p):
		m = Mooshimeter(p)
		m.connect()
		# Apply some default settings
		m.meter_settings.setBufferDepth(32) #samples
		m.meter_settings.setSampleRate(125) #Hz
		m.meter_settings.setHVRange(60) #volts
		# Calculate the mean
		m.meter_settings.calc_settings |= m.meter_settings.METER_CALC_SETTINGS_MEAN
		# Calculate the RMS as well
		m.meter_settings.calc_settings |= m.meter_settings.METER_CALC_SETTINGS_MS
		# Ensure we don't accidentally tell the Mooshimeter to reboot
		m.meter_settings.target_meter_state = m.meter_settings.present_meter_state
		# Send the ADC settings
		m.meter_settings.write()
		# Set the meter state
		m.meter_settings.target_meter_state = m.meter_settings.METER_RUNNING
		def notifyCB():
			#This will be called every time a new sample is received
			print ""
			print "Connection: ", m.p.conn_handle
			print "read A"
			print "pga(0) %f"%(m.meter_settings.chset[0] >> 4)
			tmp_meas_Iraw=m.meter_sample.reading_lsb[0]
			tmp_meas_A=m.lsbToNativeUnits(m.meter_sample.reading_lsb[0],0)
			tmp_meas_A_kaje= float(m.meter_sample.reading_lsb[0]) / 416000
			tmp_unit_A=m.getUnits(0)
			print "read V"
			print "pga(1) %f"%(m.meter_settings.chset[1] >> 4)
			tmp_meas_Uraw=m.meter_sample.reading_lsb[1]
			tmp_meas_V=m.lsbToNativeUnits(m.meter_sample.reading_lsb[1],1)
			tmp_meas_V_kaje= float(m.meter_sample.reading_lsb[1]) / 54615.2
			tmp_unit_V=m.getUnits(1)
			print ""
			print "%+.3f"%tmp_meas_A, tmp_unit_A
			print "%+.3f"%(tmp_meas_A*8), tmp_unit_A, " x8"
			print "0x%06X"%(m.meter_sample.reading_lsb[0])
			print ""
			print "%+.3f"%tmp_meas_V, tmp_unit_V
			print "0x%06X"%(m.meter_sample.reading_lsb[1])
			print ""
			print "Kaje:"
			print "%+4.3f"%(tmp_meas_A_kaje*1000), "m", tmp_unit_A, " Kaje"
			print "%+4.3f"%(tmp_meas_V_kaje*1000), "m", tmp_unit_V, " Kaje"
			print ""

			sTime=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
			sLine=sTime + "; AKaje=%.6f;"%tmp_meas_A_kaje + " VKaje=%.6f;"%tmp_meas_V_kaje + " Iraw=%i;"%tmp_meas_Iraw  + " Uraw=%i;"%tmp_meas_Uraw 
			print sLine
			logfile.write(sLine + "\n")
			logfile.flush()
		# Enable streaming
		m.meter_sample.enableNotify(True,notifyCB)
		m.meter_settings.write()
		return m

	# Connect to the meter with the strongest signal
	meters = sorted(meters, key=attrgetter('rssi'),reverse=True)
	myMoo = connectToMeterAndStream(meters[0])
	try:
		while True:
			# This call checks the serial port and processes new data
			BGWrapper.idle()
	except KeyboardInterrupt:
		#print "myMoo.disconnect()"
		#myMoo.disconnect() << this gives an error
		print "BGWrapper.disconnect()"
		BGWrapper.disconnect()
		print "done"
		pass
	
