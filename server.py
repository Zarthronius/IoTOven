from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO

## Pin values
mq2Pin = 38     # GPIO 20
flamePin = 40   # GPIO 21
heaterPin = 22

GPIO.setmode(GPIO.BOARD)
# Heater GPIO
GPIO.setup(22, GPIO.OUT)
# Gas sensor GPIO
GPIO.setup(mq2Pin, GPIO.IN)
# Flame sensor GPIO
GPIO.setup(flamePin, GPIO.IN)
Request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global Request
    # Handshaking connection with app
    messagetosend = bytes('Hi !',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    print(Request)
    # Turn heater on/off after requests from app
    if Request == 'start':
      GPIO.output(heaterPin,True) 
    if Request == 'stop':
      GPIO.output(heaterPin,False)

    # Turn off heat in case of fire, can be altered to shut down entire oven
    if GPIO.input(flamePin) == GPIO.LOW:
      print ('Warning: flame detected. Turning heater off.')
      GPIO.output(heaterPin,False)

    # Turn off heat in case of gas, can be altered to shut down entire oven
    if GPIO.input(mq2Pin) == GPIO.LOW:
      print ('Warning: gas detected. Turning heater off.')
      GPIO.output(heaterPin,False)
    return

## Create HTTP server
# Local IP address
server_address_httpd = ('192.168.157.179',8080) 
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting server ...')
httpd.serve_forever()
GPIO.cleanup()
