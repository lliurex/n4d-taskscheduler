#!/usr/bin/python3
#Copyright 2023 LliureX Team
#GPL-3 Licensed https://www.gnu.org/licenses/gpl-3.0.txt
#N4d module for accesing taskscheduler API

import os,socket
import threading
import time
from  datetime import date
import signal
import n4d.responses
import n4d.client as n4dclient
import n4d.server.core as n4dCore
import taskscheduler.taskscheduler as taskscheduler
				
class SchedulerClient():
	def __init__(self):
		self.dbg=False
		self.task_prefix='remote-' #Temp workaround->Must be declared on a n4d var
		self.cron_dir='/etc/cron.d'
		self.count=0
		self.holidays_shell="/usr/bin/check_holidays.py"
		self.pidfile="/tmp/taskscheduler.pid"
		self.core=n4dCore.Core.get_core()
		self.main_thread_timer=60
		self.taskcheduler=taskscheduler.TaskScheduler()
		#self.n4dclient=self._n4d_connect('localhost')
	#def __init__
				
	def startup(self,options):
		t=threading.Thread(target=self._main_thread)
		t.daemon=True
		t.start()
	#def startup

	def _debug(self,msg):
		if self.dbg:
			print("{}".format(msg))
	#def _debug

	def _main_thread(self):
		self.core.register_variable_trigger("SCHEDULED_TASKS","SchedulerClient",self.process_tasks)
		tries=10
		for x in range (0,tries):
			#self.scheduler_var=objects["VariablesManager"].get_variable("SCHEDULED_TASKS")
			self.scheduler_var=self.core.get_variable("SCHEDULED_TASKS")["return"]
			if self.scheduler_var!=self.count:
				self.count=self.scheduler_var
				self.process_tasks()
			else:
				time.sleep(self.main_thread_timer)
	#def _main_thread

	def process_tasks(self,data=None):
	#In origin this function read the json tasks and populates the according cron files
	#New version doesn't have json so simply read the server (if we're on a client) tasks
		self._debug("DEPRECATED Processings tasks")
		self._debug("V2 don't needs to process anything")
		return n4d.responses.build_successful_call_response()
	#def process_tasks

