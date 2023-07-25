#!/usr/bin/python3
#Copyright 2023 LliureX Team
#GPL-3 Licensed https://www.gnu.org/licenses/gpl-3.0.txt
#N4d module for accesing taskscheduler API (Server side)

import os
import json
from  datetime import date
import taskscheduler.taskscheduler as taskscheduler
import n4d.responses
import n4d.server.core as n4dCore
from n4d.utils import n4d_mv

class SchedulerServer():
	def __init__(self):
		self.dbg=True
		self.tasks_dir="/etc/scheduler/tasks.d"
		self.available_tasks_dir="/etc/scheduler/conf.d/tasks"
		self.conf_dir="/etc/scheduler/conf.d/"
		self.conf_file="%s/scheduler.conf"%self.conf_dir
		self.n4dCore=n4dCore.Core.get_core()
		self.taskscheduler=taskscheduler.TaskScheduler()
	#def __init__

	def _debug(self,msg):
		if (self.dbg):
			print("Scheduler: %s" %msg)
	#def _debug

	def get_local_tasks(self):
	#This function is for compat with BellScheduler only. 
	#It fakes the output of the old n4d server plugin
		output={"BellScheduler":{}}
		tasks=self.taskscheduler.getSystemCron()
		for key,item in tasks.items():
			#The bellID is the last parm if "bellscheduler" in line
			if "BellSchedulerPlayer" in item.get("cmd",""):
				bellId=item["cmd"].split(" ")[-1]
				item["BellId"]=str(bellId)
				output["BellScheduler"].update({bellId:item})
		self._debug("OUTPUT: {}".format(output))
		return n4d.responses.build_successful_call_response(output)
	#def get_local_tasks
			
	def write_tasks(self,*args):
	#This function is for compat with BellScheduler only. 
	#It fakes the input of the old n4d server plugin
		inputTask=args[-1]
		cronArray=[]
		for key,taskline in inputTask.items():
			if key=="BellScheduler":
				print(taskline)
				for taskKey,task in taskline.items():
					line="{0} {1} {2} {3} {4} root {5}".format(task.get("m",0),task.get("h",0),task.get("dom",1),task.get("mon",1),task.get("dow",1),task.get("cmd",""))
					cronArray.append(line)
					print(line)
				self.taskscheduler.writeSystemCron(cronArray,"localBellScheduler")
		return n4d.responses.build_successful_call_response()
	#def write_tasks

	def remove_task(self,task,*args):
	#This function is for compat with BellScheduler only. 
	#It fakes the input of the old n4d server plugin
		if len(args)==3:
			if args[0]=="BellScheduler":
				cronF=os.path.join("/","etc","cron.d","localBellScheduler")
				bellId=args[1]
				cmd=args[2]
				self._debug("Removing bellId {}".format(bellId))
				cron=[]
				with open(cronF,"r") as fh:
					for line in fh.readlines():
						print(line.split()[-1].strip())
						if line.split()[-1].strip()!=str(bellId):
							self._debug(cron.append(line))
				with open(cronF,"w") as fh:
					fh.writelines(cron)
		return n4d.responses.build_successful_call_response()
	#def remove_task

#class SchedulerServer
