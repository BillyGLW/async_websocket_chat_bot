from routines.threadpool import Pool

from settings import *

import asyncio

import logging as log

if DEBUG:
	logging = log.getLogger()
	logging.root.setLevel(log.NOTSET)
	log.basicConfig(level=log.NOTSET)

def main():
	result_dict = {}
	pool = Pool(200) # where 1 is meant to be the number of the workers
	# asyncio.get_event_loop().run_until_complete(pool.start(connection_data, result_dict))
	pool.start(connection_data, result_dict)
	
if __name__ == '__main__':
	main()