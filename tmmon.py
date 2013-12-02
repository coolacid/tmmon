#!/usr/bin/python

import sys, time, urllib2, json
#from btcexchange import *
from PyQt4 import QtGui, QtCore

class TMMon(QtGui.QWidget):
    def __init__(self, tmkey, updatespeed):
        super(TMMon, self).__init__()
	self.TMKey = tmkey
	self.updatespeed = updatespeed
	self.Worker = []
	self.WorkerValue = []
	self.initUI()

    def initUI(self):
	i=0
	spacing = 25
        self.center()
        self.setWindowTitle('TripleMining Monitor')
	font = QtGui.QFont()
	font.setPointSize(16)

	url = "http://api.triplemining.com/json/stats"
	try:
	    req = urllib2.Request(url)
	    res = urllib2.urlopen(req)
	    result = json.load(res)
	except urllib2.HTTPError as e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ', e.code
	except urllib2.URLError as e:
	    print 'We failed to reach a server.'
	    print 'Reason: ', e.reason
	print result

	self.PoolUsers = QtGui.QLabel("Pool Users:", self)
	self.PoolUsersValue = QtGui.QLabel("%d" % (int(result['users'])), self)
	self.PoolUsers.move (15, 5+(spacing))
	self.PoolUsersValue.move (300,5+(spacing))
	self.PoolUsers.setFont(font)
	self.PoolUsersValue.setFont(font)
	self.PoolUsersValue.setFixedWidth(200)

	self.PoolHash = QtGui.QLabel("Pool Hashrate:", self)
	self.PoolHashValue = QtGui.QLabel("%.2f" % (float(result['hashrate'])), self)
	self.PoolHash.move (15, 5+(2*spacing))
	self.PoolHashValue.move (300,5+(2*spacing))
	self.PoolHash.setFont(font)
	self.PoolHashValue.setFont(font)
	self.PoolHashValue.setFixedWidth(200)

	self.PoolShares = QtGui.QLabel("Pool Shares:", self)
	self.PoolSharesValue = QtGui.QLabel("%d" % (int(result['solved'])), self)
	self.PoolShares.move (15, 5+(3*spacing))
	self.PoolSharesValue.move (300,5+(3*spacing))
	self.PoolShares.setFont(font)
	self.PoolSharesValue.setFont(font)
	self.PoolSharesValue.setFixedWidth(200)

	url = "http://api.triplemining.com/json/%s" % self.TMKey
	try:
	    req = urllib2.Request(url)
	    res = urllib2.urlopen(req)
	    result = json.load(res)
	except urllib2.HTTPError as e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ', e.code
	except urllib2.URLError as e:
	    print 'We failed to reach a server.'
	    print 'Reason: ', e.reason
	print result

	self.Reward = QtGui.QLabel("Confirmed Reward:", self)
	self.RewardValue = QtGui.QLabel("%.8f" % (float(result['confirmed_reward'])), self)
	self.Reward.move (15, 5+(5*spacing))
	self.RewardValue.move (300,5+(5*spacing))
	self.Reward.setFont(font)
	self.RewardValue.setFont(font)
	self.RewardValue.setFixedWidth(200)

	self.EReward = QtGui.QLabel("Estimated Reward:", self)
	self.ERewardValue = QtGui.QLabel("%.8f" % (float(result['estimated_payout'])), self)
	self.EReward.move (15, 5+(6*spacing))
	self.ERewardValue.move (300,5+(6*spacing))
	self.EReward.setFont(font)
	self.ERewardValue.setFont(font)
	self.ERewardValue.setFixedWidth(200)

	self.HashRate = QtGui.QLabel("Total Hashrate:", self)
	self.HashRateValue = QtGui.QLabel("%d" % (int(result['hashrate'])), self)
	self.HashRate.move (15, 5+(7*spacing))
	self.HashRateValue.move (300,5+(7*spacing))
	self.HashRate.setFont(font)
	self.HashRateValue.setFont(font)
	self.HashRateValue.setFixedWidth(200)

	for worker, value in result['workers'].iteritems():
	    self.Worker.append(QtGui.QLabel("%s:" % (worker), self))
	    self.WorkerValue.append(QtGui.QLabel("%s" % (value["shares"]), self))
	    self.Worker[i].move (15, 5+((i+9)*spacing))
	    self.WorkerValue[i].move (300,5+((i+9)*spacing))
	    self.Worker[i].setFont(font)
	    self.WorkerValue[i].setFont(font)
	    self.WorkerValue[i].setFixedWidth(200)
	    i += 1

        self.resize(450, 22+((i+10)*22))
	self.show()

	QtCore.QTimer.singleShot(self.updatespeed*1000,self.updateTickers)

    def updateTickers(self, preload=0):
	i=0
	RED = QtGui.QPalette()
	RED.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
	GREEN = QtGui.QPalette()
	GREEN.setColor(QtGui.QPalette.Foreground,QtCore.Qt.darkGreen)

	print "TICK"

	url = "http://api.triplemining.com/json/stats"
	try:
	    req = urllib2.Request(url)
	    res = urllib2.urlopen(req)
	    result = json.load(res)
	except urllib2.HTTPError as e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ', e.code
	except urllib2.URLError as e:
	    print 'We failed to reach a server.'
	    print 'Reason: ', e.reason
	print result

	self.PoolUsersValue.setText("%d" % (int(result['users'])))
	self.PoolHashValue.setText("%.2f" % (float(result['hashrate'])))
	self.PoolSharesValue.setText("%d" % (int(result['solved'])))

	url = "http://api.triplemining.com/json/%s" % self.TMKey
	try:
	    req = urllib2.Request(url)
	    res = urllib2.urlopen(req)
	    result = json.load(res)
	except urllib2.HTTPError as e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ', e.code
	except urllib2.URLError as e:
	    print 'We failed to reach a server.'
	    print 'Reason: ', e.reason
	print result

	self.RewardValue.setText("%.8f" % (float(result['confirmed_reward'])))
	self.ERewardValue.setText("%.8f" % (float(result['estimated_payout'])))
	self.HashRateValue.setText("%d" % (int(result['hashrate'])))

	for worker, value in result['workers'].iteritems():
	    self.WorkerValue[i].setText("%s" % (value["shares"]))
	    if value['alive'] == "true":
		self.WorkerValue[i].setPalette(GREEN)
	    else:
		self.WorkerValue[i].setPalette(RED)

	QtCore.QTimer.singleShot(self.updatespeed*1000,self.updateTickers)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  

def main(tmkey, updatespeed):
    app = QtGui.QApplication(sys.argv)
    ex = TMMon(tmkey,updatespeed)
    sys.exit(app.exec_())


if __name__ == '__main__':
    #exchanges = [["GOX", "BTCUSD"],["BFX", "BTCUSD"],["BFX", "LTCUSD"]]
    conf = open("tmkey.txt", "r")
    for line in conf:
	tmkey=line.strip()
    conf.close
    main(tmkey, 60)
