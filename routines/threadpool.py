import asyncio
from workers.wss_worker_chat import WSS_Worker
import logging
import threading
from settings import (number_of_threads)

class Pool(object):
	def __init__(self, workers_obj):
		self.workers_obj = workers_obj
		self.workers_dict = self.get_workers_dict


	def start(self, connection_data, result_dict):
		for i, worker in self.workers_dict.items():
			logging.info("Worker %d started: %s" % (i, str(worker)))
			# https://bugs.python.org/issue22239 problem , temp solution:
			"""
			import nest_asyncio
			nest_asyncio.apply()
			"""
			for thread in range(number_of_threads):
				print("Worker %d started: %s" % (i, str(worker)))
				threading.Thread(target=worker[0].worker).start()
	
	@property
	def get_workers_dict(self):
		workers = {}
		for i in range(1, self.workers_obj + 1):
			workers[i] = [WSS_Worker(i), asyncio.new_event_loop()]
		return workers
