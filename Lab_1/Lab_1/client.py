import os
import socket
import sys
import uuid
from time import sleep
from PIL import Image
from matplotlib import pylab

def toGrayscale(path):
    imgGray = Image.open(path).convert('LA')
    if not os.path.exists("data"):
        os.mkdir("data")
    newPath = os.path.join("data", f"{uuid.uuid4()}.png")
    imgGray.save(newPath)
    return newPath

def showImage(path, description):
    pylab.title(description)
    pylab.imshow(Image.open(path))
    pylab.axis("off")
    pylab.show()

class Client:

    def __init__(self, serverPort, host, chunkSize):
        self.__socket = None
        self.__host = host
        self.__port = serverPort
        self.__chunk = chunkSize

    def send(self, path):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
            file = open(path, "rb")

            fileSize = os.path.getsize(path)
            print(f"File size on client: {fileSize} bytes.")
            print("Start sending...")

            data = file.read(self.__chunk)
            sendSize = 0
            while data:
                self.__socket.send(data)
                data = file.read(self.__chunk)
                sendSize += sys.getsizeof(data)
                print(f"Progress: ({round(sendSize / fileSize * 100, 2)}%)")

            print("Complete sending.")
            file.close()
        except ConnectionRefusedError as error:
            print(error.__str__())
        finally:
            self.__socket.close()


def run(host, port, chunkSize):
    print(f"Client start at port: {port}")
    client = Client(port, host, chunkSize)

    while True:
        try:
            imgPath: str = input("Write path to image: ")
            grayImgPath = toGrayscale(imgPath)
            showImage(grayImgPath, "Initial image (client)")
            client.send(grayImgPath)
            sleep(10)
        except FileNotFoundError:
            print("File not found.")




