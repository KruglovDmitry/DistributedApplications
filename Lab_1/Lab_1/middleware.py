import os.path
import socket
import sys
import tempfile
import uuid

import numpy as np
from PIL import Image
import random

def addNoise(img):
    row, col = img.shape
    pixels = random.randint(300, 10000)
    for i in range(pixels):
        x = random.randint(0, col - 1)
        y = random.randint(0, row - 1)
        img[y][x] = 255

    pixels = random.randint(300, 10000)
    for i in range(pixels):
        x = random.randint(0, col - 1)
        y = random.randint(0, row - 1)
        img[y][x] = 0

    return img

class Middleware:

    def __init__(self, host, clientPort, serverPort, chunkSize):
        self.__sender = None
        self.__listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__client_port = clientPort
        self.__server_port = serverPort
        self.__chunk = chunkSize
        self.__temp = tempfile.gettempdir()
        self.__path = ""

    def __del__(self):
        self.__listener.close()

    def listen(self):
        print(f"Middleware listening on: {self.__host}:{self.__client_port}")
        self.__listener.bind((self.__host, self.__client_port))
        self.__listener.listen()

    def __upload(self):
        clientSocket, clientAddress = self.__listener.accept()
        filePath = os.path.join(self.__temp, f"{uuid.uuid4()}.png")
        file = open(filePath, "wb")
        data = clientSocket.recv(self.__chunk)

        print("Starting receiving data...")

        fileSize = 0
        while data:
            file.write(data)
            fileSize += sys.getsizeof(data)
            print(f"Receive data: {fileSize} bytes")
            data = clientSocket.recv(self.__chunk)
            if sys.getsizeof(data) < self.__chunk:
                print(f"Image size not equals chunk size: {sys.getsizeof(data)} bytes")

        print("Receiving data complete.")
        file.close()
        clientSocket.close()
        self.__path = filePath

    def __noise(self):
        if len(self.__path) == 0:
            print("Image not snapped up.")
            return
        else:
            result = addNoise(np.array(Image.open(self.__path).convert('L')))
            self.__path = os.path.join(self.__temp, f"{uuid.uuid4()}.png")
            Image.fromarray((result).astype(np.uint32)).save(self.__path)

    def handle(self):
        self.__upload()
        self.__noise()

        self.__sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sender.connect((self.__host, self.__server_port))

        file = open(self.__path, "rb")
        fileSize = os.path.getsize(self.__path)
        print("Start sending...")

        data = file.read(self.__chunk)
        sendingSize = 0
        while data:
            self.__sender.send(data)
            data = file.read(self.__chunk)
            sendingSize += sys.getsizeof(data)
            print(f"Progress: ({round(sendingSize / fileSize * 100, 2)}%)")

        print("Complete sending.")

        file.close()
        self.__sender.close()


def run(host, clientPort, serverPort, chunkSize):
    middleware = Middleware(host, clientPort, serverPort, chunkSize)
    middleware.listen()
    while True:
        middleware.handle()




