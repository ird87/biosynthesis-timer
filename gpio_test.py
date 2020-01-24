#!/usr/bin/python
import inspect
import os

class GPIO(object):
	"""docstring"""

	"""Конструктор класса. Поля класса"""
	def __init__(self, ports):
		# Список заявленных к работе портов
		self.ports = ports

	"""Метод включаем подачу напряжения на указанный порт"""
	def port_on(self, port):
		# проверяем, что порт указан
		if port > 0:
			print('Включаем подачу напряжения на ' + str(port) + ' порт')

	"""Метод отключает подачу напряжения на указанный порт"""
	def port_off(self, port):
		# проверяем, что порт указан
		if port > 0:
			print('Отключаем подачу напряжения на ' + str(port) + ' порт')