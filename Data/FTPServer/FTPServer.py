# Author: Gabriel Dinse
# File: FTPServer.py
# Date: 11/27/2020
# Made with PyCharm

# Standard Library
import os

# Third party modules
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Local application imports


def main():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Templates")
    os.chdir(path)

    ip_address_and_port = ("localhost", 2121)
    authorizer = DummyAuthorizer()
    authorizer.add_user("admin", "admin", '.', perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(ip_address_and_port, handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
