from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import pigpio

PIN=14
OPEN=1550
CLOSE=1150
DURATION=0.25

HOSTNAME = "localhost"
PORT = 80
PI = pigpio.pi()

def open():
	PI.set_servo_pulsewidth(PIN, OPEN)

def close():
	PI.set_servo_pulsewidth(PIN, CLOSE)

def dispense():
	open()
	time.sleep(DURATION)
	close()

class HoneyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/treat':
			dispense()
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(bytes("Happy Honey!", "utf-8"))
		else:
			self.send_response(404)
			self.end_headers()

if __name__ == "__main__":
	close()
	webServer = HTTPServer((HOSTNAME, PORT), HoneyServer)
	print("Server started!")

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")

