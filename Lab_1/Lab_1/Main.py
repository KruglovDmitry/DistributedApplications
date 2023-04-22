from time import sleep
from threading import Thread
import client, middleware, server

host = "127.0.0.1"
serverPort = 8000
clientPort = 8001
chunkSize = 2048

server = Thread(target = server.run, args=(host, serverPort, chunkSize,))
middleware = Thread(target = middleware.run, args=(host, clientPort, serverPort, chunkSize,))
client = Thread(target = client.run, args=(host, clientPort, chunkSize,))

server.start()
sleep(1)
middleware.start()
sleep(1)
client.start()
