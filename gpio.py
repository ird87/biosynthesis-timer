#!/usr/bin/python
import inspect
import os
import sys
import RPi.GPIO as GPIO

class GPIO(object):
	"""docstring"""

	"""Конструктор класса. Поля класса"""
	def __init__(self, ports):
		import RPi.GPIO as GPIO
		self.gpio = GPIO
		self.gpio.setmode(GPIO.BOARD)
		self.ports = ports
		# установки GPIO
		self.gpio.setup(self.ports, GPIO.OUT, initial = GPIO.LOW)

	"""Метод включаем подачу напряжения на указанный порт"""
	def port_on(self, port):
		# проверяем, что порт указан
		if port > 0:
			self.gpio.output(port, True)

	"""Метод отключает подачу напряжения на указанный порт"""
	def port_off(self, port):
		# проверяем, что порт указан
		if port > 0:
			self.gpio.output(port, False)