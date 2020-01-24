#! /usr/bin/env python
# -*- coding: utf-8 -*-

import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from timer import Ui_wBiosynthesisTimer
import sys

from conf import Configure
from process import TimerMode, ValveStatus, Process
 
class TimerWindow(PyQt5.QtWidgets.QMainWindow):
	progressbar_change = PyQt5.QtCore.pyqtSignal(int)
	progressbar_set = PyQt5.QtCore.pyqtSignal(int)
	valve_status_set = PyQt5.QtCore.pyqtSignal(ValveStatus)
	time_change =  PyQt5.QtCore.pyqtSignal(str)

	def __init__(self):
		super(TimerWindow, self).__init__()
		self.ui = Ui_wBiosynthesisTimer()
		self.ui.setupUi(self)
		self.setFixedSize(360, 260)
		self.center()
		self.setWindowFlags(
		Qt.Window |
		Qt.CustomizeWindowHint |
		Qt.WindowTitleHint |
		Qt.WindowCloseButtonHint |
		Qt.WindowStaysOnTopHint |
		Qt.WindowMinimizeButtonHint
		)

		
		self.conf=Configure()

		try:
			from gpio import GPIO
			self.test_environment = False
		except (ImportError, RuntimeError):			
			from gpio_test import GPIO
			self.test_environment = True
			print('TestModeON')

		self.gpio=GPIO([self.conf.port])
		self.process=Process(self)
		self.mode=TimerMode.ManualMode
		self.status=ValveStatus.ValveOpen

		# По-умолчанию скрываем группу с автоматическим режимом управления
		self.ui.gbManualMode.setVisible(False)
		self.ui.lblManualTimer.setVisible(False)

		# Назначим команды кнопкам
		self.ui.btnAutoStart.clicked.connect(self.auto_mode_start)
		self.ui.btnAutoStop.clicked.connect(self.auto_mode_stop)
		self.ui.btnManualStart.clicked.connect(self.manual_mode_start)
		self.ui.btnManualStop.clicked.connect(self.manual_mode_stop)
		self.ui.cmbCurrentMode.currentIndexChanged.connect(self.current_mode_changed) 
		self.progressbar_change.connect(self.change_progressbar, PyQt5.QtCore.Qt.QueuedConnection)
		self.progressbar_set.connect(self.set_progressbar, PyQt5.QtCore.Qt.QueuedConnection)
		self.valve_status_set.connect(self.set_status, PyQt5.QtCore.Qt.QueuedConnection)
		self.time_change.connect(self.change_time, PyQt5.QtCore.Qt.QueuedConnection)
		


	def center(self):
		# geometry of the main window
		qr = self.frameGeometry()
		# center point of screen
		cp = QDesktopWidget().availableGeometry().center()
		# move rectangle's center point to screen's center point
		qr.moveCenter(cp)
		# top left of rectangle becomes top left of window centering it
		self.move(qr.topLeft())

	def	current_mode_changed(self):
		# Включаем ручной режим: выключаем автоматический / меняем видимую группу в ui / Устанавливаем режим
		if self.ui.cmbCurrentMode.currentIndex()==0:
			self.auto_mode_stop()
			self.ui.gbAutoMode.setVisible(False)
			self.ui.gbManualMode.setVisible(True)
			self.set_mode(TimerMode.ManualMode)
		# Включаем автоматический режим: выключаем ручной / меняем видимую группу в ui / Устанавливаем режим
		if self.ui.cmbCurrentMode.currentIndex()==1:
			self.manual_mode_stop()
			self.ui.gbAutoMode.setVisible(True)
			self.ui.gbManualMode.setVisible(False)
			self.set_mode(TimerMode.AutoMode)

	def auto_mode_start(self):
		self.process.start()

	def auto_mode_stop(self):
		self.process.process_break()

	def manual_mode_start(self):
		self.set_status(ValveStatus.ValveClose)
		self.gpio.port_on(self.conf.port)

	def manual_mode_stop(self):
		self.set_status(ValveStatus.ValveOpen)
		self.gpio.port_off(self.conf.port)

	def set_mode(self, mode):
		self.mode=mode
		self.set_status(ValveStatus.ValveOpen)

	def set_status(self, status):
		self.status=status
		if self.status == ValveStatus.ValveOpen:
			self.ui.txtCurrentStatus.setText('клапан открыт')
		if self.status == ValveStatus.ValveClose:
			self.ui.txtCurrentStatus.setText('клапан закрыт')

	def set_progressbar(self, maximum):
			self.ui.pbrProgressBar.setValue(0)
			self.ui.pbrProgressBar.setMaximum(maximum)

	def change_time(self, t):
			self.ui.lblTimer.setText(t)

	def change_progressbar(self, t):
		if self.ui.pbrProgressBar.value() < self.ui.pbrProgressBar.maximum():
			self.ui.pbrProgressBar.setValue(self.ui.pbrProgressBar.value() + t)

	def closeEvent(self, event):
		self.set_status(ValveStatus.ValveOpen)
		self.gpio.port_off(self.conf.port)


 
def main():
	app = PyQt5.QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = TimerWindow()  # Создаём объект класса Main
	window.show()  # Показываем окно
	app.exec_()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()