# websocket bot / wss (ws via tls)

### creating self-signed certificate on purpose of wss client
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem