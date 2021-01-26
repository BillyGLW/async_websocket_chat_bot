import asyncio
import websockets
import logging as log
import queue
import json

from settings import (timeout, connection_data)

from opcodes import opcode


class WSS_Worker(object):
	def __init__(self, uuid):
		self.server_client_id = None
		self.server_cliend_ceid = 0
		self.server_conn_id = None
		self.server_hash = None
		self.id = uuid

	def worker(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.work(connection_data))
		return

	async def work(self, connection_data):
		uri = connection_data['wss']
		history_messages = list()
		task_queue = queue.Queue()
		data_send_queue = queue.Queue()
		async with websockets.connect(uri, extra_headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
								"Accept": "*/*",
								"Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
								"Accept-Encoding": "gzip, deflate",
								"Origin": "https://6obcy.org",
								"DNT": 1,
								"Connection": "keep-alive, Upgrade",
								"Pragma": "no-cache",
								"Cache-Control": "no-cache",
								}) as websocket:


			while(True):
				try:
					message_str = await asyncio.wait_for(websocket.recv(), timeout=timeout)
					task_queue.put_nowait(message_str)
					server_message = task_queue.get()
					log.info("Server: %s" % server_message)
					
					if "ckey" in server_message:
						server_response_client = json.loads(server_message[1:])
						self.server_client_id = server_response_client['ev_data']['ckey']
						print("[*] Got new connection: {}".format(self.server_client_id))
					elif "hash" in server_message:
						server_message_json = json.loads(server_message[1:])
						self.server_conn_id = server_message_json['ev_data']['conn_id']
						self.server_hash = server_message_json['ev_data']['hash']
					elif "msg" in server_message:
						msg_formatted = json.loads(server_message[1:])
						print("[*] {}. Got new message: {}".format(self.id, msg_formatted['ev_data']['msg']))
						history_messages.append(msg_formatted)
						if self.server_client_id:
							user_message = "hej"
							if user_message:
								_routine_send = '4{"ev_name":"_mtyp","ev_data":{"ckey":"xyz","val":true}}'
								_routine_send_json = json.loads(_routine_send[1:])
								_routine_send_json['ev_data']['ckey'] = self.server_client_id
								await websocket.send(opcode['connect'] + json.dumps(_routine_send_json))

								response_text = json.loads('{"ev_name":"_pmsg","ev_data": {"ckey":"","msg":"","idn":0},"ceid":2}')
								response_text['ev_data']['ckey'] = self.server_client_id
								response_text['ev_data']['msg'] = "k16"
								await websocket.send(opcode['connect'] + json.dumps(response_text))
						else:
							log.info("[!] No client info, returning...")
							pass
					# elif "begacked" in server_message:
					# 	server_message_json = json.loads(server_message[1:])
					# 	self.server_cliend_ceid = server_message_json['ceid']
					elif '"ev_name":"sdis"' in server_message:
						self.server_client_id = None
						log.info("[!] Disconnected.. searching for next connection..")
						await websocket.send(opcode['disconnect'])
					elif not self.server_client_id and self.server_conn_id and self.server_hash:
						log.info("[*] Connecting with new peer...")
						msg = '4{"ev_name":"_sas","ev_data":{"channel":"main","myself":{"sex":0,"loc":0},"preferences":{"sex":0,"loc":0}},"ceid":1}'
						chat_text = await websocket.send(msg)

				except asyncio.TimeoutError:
					log.warn("timeout error - no data in {} seconds, pinging connection".format(timeout))
					await asyncio.wait_for(pong_waiter, timeout=2)
					log.warn("ping/pong received, keeping connection alive...")
				except Exception as e:
					error_message = "resseting connection: {}".format(e.args)
					log.error(error_message)
					raise Exception(error_message)

if __name__ == '__main__':
	main()