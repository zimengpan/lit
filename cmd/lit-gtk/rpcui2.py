#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

#Extend the library search path to our `qt_files` directory
import sys
sys.path.append("qt_files") 

import socket
import json

#ui file import 
import rpcui_ui

#Handles rpc communications and conjugate response handler functions
class rpcCom():
    def __init__(self, addr, port):

        #Open up the socket connection
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((addr, port))

    def getBal(self):
        rpcCmd = {
            "method": "LitRPC.Bal",
            "params": [{
            }]
        }
        #TODO: What is the purpose of this `id`
        rpcCmd.update({"jsonrpc": "2.0", "id": "93"})

        print json.dumps(rpcCmd)
        self.conn.sendall(json.dumps(rpcCmd))

        r = json.loads(self.conn.recv(8000000))
        print r

        return r["result"]["TxoTotal"]

    def getAdr(self):
        rpcCmd = {
		   "method": "LitRPC.Address",
		   "params": [{"NumToMake": 0}]
	}

	rpcCmd.update({"jsonrpc": "2.0", "id": "94"})

	print json.dumps(rpcCmd)
	self.conn.sendall(json.dumps(rpcCmd))

	r = json.loads(self.conn.recv(8000000))
	print r

	return r["result"]["Addresses"][-1]

    def prSend(self, adr, amt):
	rpcCmd = {
		   "method": "LitRPC.Send",
		   "params": [{"DestAddrs": [adr], "Amts": [amt]}]
	}

	rpcCmd.update({"jsonrpc": "2.0", "id": "95"})

	print json.dumps(rpcCmd)
	self.conn.sendall(json.dumps(rpcCmd))

	r = json.loads(self.conn.recv(8000000))
	print r

	if r["error"] != None:
            return "send error: " + r["error"]

	return "Sent. TXID: " + r["result"]["Txids"][0]

class mainWindow(QtGui.QMainWindow, rpcui_ui.Ui_MainWindow):
    def __init__(self, parent):
        #Set up calls to get QT working
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        #There is no need for a hint button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        #Set up the RPC communication object
        self.rpcCom = rpcCom("127.0.0.1", 9750)

        #Setup the connections to their triggers
        self.setup_connections()

    #Sets the text value for the balance label. Make this its own function to 
    # be used as a callback for the "Refresh" button
    def setBalLabel(self):
        bal = self.rpcCom.getBal()
        self.bal_label.setText(str(bal))

    def setup_connections(self):
        #Populate the address label
        addr = self.rpcCom.getAdr()
        self.addr_label.setText(addr);

        #Populate the balance label
        self.setBalLabel()

        #Set the trigger for the "Refresh" button
        self.bal_refresh_button.clicked.connect(self.setBalLabel)


def main(args):
    app = QtGui.QApplication(args)
    window = mainWindow(None)

    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
