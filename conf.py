#!/usr/bin/python
import configparser
import os

class Configure(object):

	def __init__(self):
		self.port = 0
		self.conf = configparser.ConfigParser()
		self.conf.read('base.conf', encoding = 'WINDOWS-1251')
		self.config()
	   
	def config(self):
		self.port =  self.conf.getint('Raspberry', 'port')
		self.time_pause =  self.conf.getint('Setting', 'time_pause')
		self.time_process =  self.conf.getint('Setting', 'time_process')
