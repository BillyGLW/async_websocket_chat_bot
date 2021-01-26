try:
	import ssl
	import pathlib
	import certifi
except Exception as e:
	raise e

timeout = 10000

connection_data = {
	"wss": "wss://server.xyz.com:7002/",
	"url": "https://xyz.org/meeting"
}

# SSL CONFIG
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
ssl_context.load_verify_locations(certifi.where())

# Logging
DEBUG = 0

# Threading
number_of_threads = 2