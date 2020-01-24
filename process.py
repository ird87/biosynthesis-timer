#!/usr/bin/python
from enum import Enum
import threading
import time

class Process(object):

	def __init__(self, main):
		self.main=main
		self.in_the_process=False


	def start(self):
		self.in_the_process=True
		self.my_thread = threading.Thread(target=self.processing)
		self.my_thread.start()


	def stop(self):
		self.in_the_process=False
		self.my_thread.join()


	def processing(self):
		try:
			while self.in_the_process:
				self.run()
				self.pause()
		except Exception as e:
			print(e.args[0])
			return

	def process_break(self):
		self.in_the_process=False

	def run(self):
		self.valve_close()
		self.main.progressbar_set.emit(self.main.conf.time_process)
		self.main.time_change.emit(str_time(self.main.conf.time_process))
		t=0
		while t < self.main.conf.time_process:
			self.check_for_interruption()
			t += 1
			time.sleep(1)
			self.main.progressbar_change.emit(1)
			self.main.time_change.emit(str_time(self.main.conf.time_process-t))

	def pause(self):
		self.valve_open()
		self.main.progressbar_set.emit(self.main.conf.time_pause)
		self.main.time_change.emit(str_time(self.main.conf.time_pause))
		t=0
		while t < self.main.conf.time_pause:
			self.check_for_interruption()
			t += 1
			time.sleep(1)
			self.main.progressbar_change.emit(1)
			self.main.time_change.emit(str_time(self.main.conf.time_pause-t))

	def valve_open(self):
		self.main.gpio.port_off(self.main.conf.port)
		self.main.valve_status_set.emit(ValveStatus.ValveOpen)
		

	def valve_close(self):
		self.main.gpio.port_on(self.main.conf.port)
		self.main.valve_status_set.emit(ValveStatus.ValveClose)

	def check_for_interruption(self):
		if not self.in_the_process:
			self.valve_open()
			self.main.progressbar_set.emit(100)
			self.main.time_change.emit(str_time(0))
			raise Exception("Abort_Type.Interrupted_by_user")

class TimerMode(Enum):
	ManualMode = 0
	AutoMode = 1

class ValveStatus(Enum):
	ValveOpen = 0
	ValveClose = 1

def str_time(t):
		format_t = time.strftime('%M:%S', time.gmtime(t))
		return format_t