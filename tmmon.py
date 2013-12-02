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
	self.Reward.move (15, 5+(spacing))
	self.RewardValue.move (300,5+(spacing))
	self.Reward.setFont(font)
	self.RewardValue.setFont(font)
	self.RewardValue.setFixedWidth(200)

	self.EReward = QtGui.QLabel("Estimated Reward:", self)
	self.ERewardValue = QtGui.QLabel("%.8f" % (float(result['estimated_payout'])), self)
	self.EReward.move (15, 5+(2*spacing))
	self.ERewardValue.move (300,5+(2*spacing))
	self.EReward.setFont(font)
	self.ERewardValue.setFont(font)
	self.ERewardValue.setFixedWidth(200)

	self.HashRate = QtGui.QLabel("Hashrate:", self)
	self.HashRateValue = QtGui.QLabel("%d" % (int(result['hashrate'])), self)
	self.HashRate.move (15, 5+(3*spacing))
	self.HashRateValue.move (300,5+(3*spacing))
	self.HashRate.setFont(font)
	self.HashRateValue.setFont(font)
	self.HashRateValue.setFixedWidth(200)

	self.TShares = QtGui.QLabel("Total Shares:", self)
	self.TSharesValue = QtGui.QLabel("%d" % (int(result['total_shares'])), self)
	self.TShares.move (15, 5+(4*spacing))
	self.TSharesValue.move (300,5+(4*spacing))
	self.TShares.setFont(font)
	self.TSharesValue.setFont(font)
	self.TSharesValue.setFixedWidth(200)


	for worker, value in result['workers'].iteritems():
	    self.Worker.append(QtGui.QLabel("%s:" % (worker), self))
	    self.WorkerValue.append(QtGui.QLabel("%s" % (value["shares"]), self))
	    self.Worker[i].move (15, 5+((i+6)*spacing))
	    self.WorkerValue[i].move (300,5+((i+6)*spacing))
	    self.Worker[i].setFont(font)
	    self.WorkerValue[i].setFont(font)
	    self.WorkerValue[i].setFixedWidth(200)
	    i += 1

        self.resize(450, 22+((i+7)*22))
	self.show()

	QtCore.QTimer.singleShot(self.updatespeed*1000,self.updateTickers)

    def updateTickers(self, preload=0):
	i=0
	RED = QtGui.QPalette()
	RED.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
	GREEN = QtGui.QPalette()
	GREEN.setColor(QtGui.QPalette.Foreground,QtCore.Qt.darkGreen)

	print "TICK"
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
	self.TSharesValue.setText("%d" % (int(result['total_shares'])))

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
