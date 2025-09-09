import http.server

# provides access to the BSD socket interface
import socket

# a framework for network servers
import socketserver

# to display a Web-based documents to users
import webbrowser

# to generate qrcode
import pyqrcode
from pyqrcode import QRCode

# convert into png format
import png

# to access operating system control
import os
#assigning port value
port=8010
#find the name of the computer user
os.environ['userprofile']
# changing the directory to access the files desktop
# with the help of os module
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),
                      'Onedrive')
os.chdir(desktop)


# creating a http request
Handler = http.server.SimpleHTTPRequestHandler
# returns, host name of the system under
# which Python interpreter is executed
hostname = socket.gethostname()


# finding the IP address of the PC
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(port)
link = IP


# converting the IP address into the form of a QRcode
# with the help of pyqrcode module

# converts the IP address into a Qrcode
url = pyqrcode.create(link)
# saves the Qrcode inform of svg
url.svg("myqr.svg", scale=8)
# opens the Qrcode image in the web browser
webbrowser.open('myqr.svg')


# Creating the HTTP request and  serving the
# folder in the PORT 8010,and the pyqrcode is generated

# continuous stream of data between client and server
with socketserver.TCPServer(("", port), Handler) as httpd:
    print("serving at port", port)
    print("Type this in your Browser", IP)
    print("or Use the QRCode")
    httpd.serve_forever()
