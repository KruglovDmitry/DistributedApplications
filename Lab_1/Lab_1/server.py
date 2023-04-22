import os
import shutil
import socket
import sys
import uuid

import numpy as np
from PIL import Image
from matplotlib import pylab

def filter(img, window = 3):

    height, width = img.shape
    mask = []
    counter = window // 2
    result = np.zeros((height, width))

    for x in range(height):
        for y in range(width):
            for i in range(window):
                if x + i - counter < 0 or x + i - counter > height - 1:
                    for j in range(window):
                        mask.append(0)
                else:
                    if y + i - counter < 0 or y + counter > width - 1:
                        mask.append(0)
                    else:
                        for j in range(window):
                            mask.append(img[x + i - counter][y + j - counter])

            mask.sort()
            result[x][y] = mask[len(mask) // 2]
            mask = []

    return result

def showImage(path, description):
    pylab.title(description)
    pylab.imshow(Image.open(path))
    pylab.axis("off")
    pylab.show()

class Server:

    def __init__(self, host, port, chunkSize):
        self.__port = port
        self.__host = host
        self.__chunk = chunkSize
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__temp = "data"
        self.__path = ""
        if not os.path.exists(self.__temp):
            os.mkdir(self.__temp)

    def __del__(self):
        self.__socket.close()
        shutil.rmtree(self.__temp, ignore_errors=True)

    def listen(self) -> None:
        print(f"Server listening on: {self.__host}:{self.__port}")
        self.__socket.bind((self.__host, self.__port))
        self.__socket.listen()

    def __upload(self):
        clientSocket, clientAddress = self.__socket.accept()
        filePath = os.path.join(self.__temp, f"{uuid.uuid4()}.png")
        file = open(filePath, "wb+")

        fileSize = 0
        data = clientSocket.recv(self.__chunk)

        print("Starting receiving data...")

        while data:
            file.write(data)
            fileSize += sys.getsizeof(data)
            print(f"Receive data: {fileSize} bytes")
            data = clientSocket.recv(self.__chunk)
            if sys.getsizeof(data) < self.__chunk:
                print(f"Image size not equals chunk size: {sys.getsizeof(data)} bytes")

        file.close()
        clientSocket.close()
        self.__path = filePath

    def __restore(self):
        if len(self.__path) == 0:
            print("Image not received.")
            return
        else:
            result = filter(np.array(Image.open(self.__path)))
            self.__path = os.path.join(self.__temp, f"{uuid.uuid4()}.png")
            Image.fromarray((result).astype(np.uint32)).save(self.__path)

    def receive(self):
        self.__upload()
        showImage(self.__path, "Image, received by server")
        self.__restore()
        showImage(self.__path, "Image, cleared by server")
        print(f"Size of data on server: {os.path.getsize(self.__path)} bytes.")


def run(host, port, chunkSize):
    server = Server(host, port, chunkSize)
    server.listen()
    while True:
        server.receive()




