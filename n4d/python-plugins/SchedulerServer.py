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
		tasks=self.taskscheduler.getSystemCron()
		output=self._filterBellSchedulerTasks(tasks)
		self._debug("OUTPUT: {}".format(output))
		return n4d.responses.build_successful_call_response(output)
	#def get_local_tasks

	def _filterBellSchedulerTasks(self,tasks):
		output={"BellScheduler":{}}
		for key,item in tasks.items():
			if "/etc/cron.d/localBellScheduler" == item.get("file","") or item.get("file","x")=="x":
				#The bellID is the last parm if "bellscheduler" in line
				if "BellSchedulerPlayer" in item.get("cmd",""):
					bellId=item["cmd"].split(" ")[-1]
					item["BellId"]=str(bellId)
					output["BellScheduler"].update({bellId:item})
		return(output)
	#def _filterBellSchedulerTasks

	def _getRawFromBellID(self,bellID):
		raw=""
		self._debug("Searching BellID: {}".format(str(bellID)))
		tasks=self.get_local_tasks()
		self._debug("RAW: {}".format(tasks))
		tasks=self.taskscheduler.getSystemCron()
		bellTasks=self._filterBellSchedulerTasks(tasks).get(str("BellScheduler"),{})
		self._debug("In data: {}".format(bellTasks))
		if str(bellID) in bellTasks.keys():
			raw=bellTasks[str(bellID)].get("raw","")
		self._debug("Get: {}".format(raw))
		return(raw)
	#def _getRawFromBellID
			
	def write_tasks(self,*args):
	#This function is for compat with BellScheduler only. 
	#It fakes the input of the old n4d server plugin
	#The new API distinguishes bewteen add/modiify 
	#checking for the presence of the original cmdline
	#So it's mandatory to get that through BellID
		inputTask=args[-1]
		cron=[]
		for key,taskline in inputTask.items():
			if key=="BellScheduler":
				self._debug("L: {}".format(taskline))
				for taskKey,task in taskline.items():
					bellTask=self._getRawFromBellID(taskKey)
					cron.append(task)
		self._debug("FULL CRON: {}".format(cron))
		self.taskscheduler.cronFromJson(cron,cronF="/etc/cron.d/localBellScheduler",orig=bellTask)
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
						if line.split()[-1].strip()!=str(bellId):
							self._debug(cron.append(line))
				with open(cronF,"w") as fh:
					fh.writelines(cron)
		return n4d.responses.build_successful_call_response()
	#def remove_task

#class SchedulerServer
