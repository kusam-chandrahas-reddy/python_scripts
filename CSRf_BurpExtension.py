#Creating Burp Extension for CSRF PoC Generator
from burp import IBurpExtender, IContextMenuFactory, ITab, ITextEditor
from java.io import PrintWriter, File, FileOutputStream
from java.lang import RuntimeException
from java.awt import Panel
from javax.swing import JScrollPane, JTextArea, JLabel, JMenuItem, JSplitPane, JFileChooser, JTextField
from burp import IHttpListener
from burp import IMessageEditorController
from java.awt import Component
from java.awt.event import ActionListener
from java.util import ArrayList
from java.util import List
from javax.swing import JScrollPane
from javax.swing import JTabbedPane
from javax.swing import JTable
from javax.swing import JButton
from javax.swing import SwingUtilities
from javax.swing.table import AbstractTableModel
from javax.swing.table import DefaultTableModel
from threading import Lock


html_poc="""<html>
<body>
<form method="{}" action="{}">
{}
<input type=submit value="Submit Form"/>
</body>
</html>
"""
input_field="""<input type="hidden" name="{}" value="{}" >"""

class ButtonListener(ActionListener):
	def __init__(self,extender):
		self.extender=extender
	def actionPerformed(self,e):
		fromButton=e.getSource().getText()
		if fromButton=='Generate HTML PoC':
			self.selectedreqid=self.extender.burptab.request_table.getSelectedRow()
			#if self.selectedreqid == -1:
			#	print('No data selected')
			#	return ""
			#self.reqservice=self.extender.burptab.data[self.selectedreqid].getHttpService()
			self.reqservice=self.extender.helpers.buildHttpService(self.extender.burptab.messageHost.getText(),int(self.extender.burptab.messagePort.getText()),self.extender.burptab.messageProtocol.getText())
			self.reqtext=self.extender.burptab.requestviewer.getMessage()
			self.analyzedreq=self.extender.helpers.analyzeRequest(self.reqservice,self.reqtext)
			self.reqparams=self.analyzedreq.getParameters()
			self.inputs=""
			for p in self.reqparams:
				print(p.getType())
				if p.getType() == p.PARAM_BODY:
					name=p.getName().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'","&#x27;")
					value=p.getValue().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'","&#x27;")
					self.inputs+=input_field.format(name,value)+'\n'
			self.htmlpoc=html_poc.format(self.analyzedreq.getMethod(),self.analyzedreq.getUrl(),self.inputs)
			self.extender.burptab.pocviewer.setText(self.htmlpoc)

		if fromButton=='Move Up':
			self.extender.burptab.pocviewer.setText("Move Up Generated!!!!!")
			pass
		if fromButton=='Move Down':
			self.extender.burptab.pocviewer.setText("Move Down Generated!!!!!")
			pass
		if fromButton=='Clear Table':
			self.extender.burptab.request_table.getModel().clearTable()
		if fromButton=='Remove Item':
			for i in self.extender.burptab.request_table.getSelectedRows():
				self.extender.burptab.request_table.getModel().removeRow(i)
			pass
		if fromButton=='HTML PoC':
			self.extender.burptab.pocviewer.setText("HTML PoC Generated!!!!!")
			pass
		if fromButton=='Generate Ajax PoC':
			self.extender.burptab.pocviewer.setText("Ajax PoC Generated!!!!!")
			pass
		if fromButton=='Save PoC':
			filesavedialog=JFileChooser()
			i=filesavedialog.showSaveDialog(None)
			if i == JFileChooser.APPROVE_OPTION:
				pocToSave=self.extender.burptab.pocviewer.getText()
				f=filesavedialog.getSelectedFile()
				fn=str(f.getName())
				if fn[-5:] != ".html" and fn[-4:] !=".htm":
					fn=fn+".html"
					rf=File(f.getParentFile(),fn)
					s=f.renameTo(rf)
					if s:
						print("Rename success")
					else:
						print("Unable to save file")
						print(s)
						print(rf.getParentFile(),rf.getName())
						print(f.getParentFile(),f.getName())
						return
				fos=FileOutputStream(f)
				fos.write(pocToSave)
				fos.close()
					
	
class MessageEditorController(IMessageEditorController):
	def __init__(self,extender):
		self.extender=extender
	def getHttpService(self):
		return self.extender.helpers.buildHttpService(self.extender.burptab.messageHost.getText(),int(self.extender.burptab.messagePort.getText()),self.extender.burptab.messageProtocol.getText())
	def getRequest(self):
		return self.extender.burptab.request_table.selectedreq.getRequest()
	def getResponse(self):
		return self.extender.burptab.request_table.selectedreq.getResponse()
	
class burptab(ITab):
	def __init__(self,extender,name):
		self.name=name
		self.extender=extender
		self.data=[]
	def getTabCaption(self):
		return self.name
	def getUiComponent(self):
		self.mainsplit=JSplitPane(JSplitPane.VERTICAL_SPLIT)
		self.split1_top=JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
		self.split2_bottom=JSplitPane(JSplitPane.VERTICAL_SPLIT)
		self.split3_bottom=JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
		self.buttonpanel = Panel()
		self.panel2 = Panel()
		self.request_table=Table(self.extender,self.data)
		self.scrollPane=JScrollPane(self.request_table)
		self.requestviewer=self.extender.callbacks.createMessageEditor(MessageEditorController(self.extender),True)
		self.pocviewer=self.extender.callbacks.createTextEditor()
		self.actionListener=ButtonListener(self.extender)
		self.buttonGeneratePoc = JButton('Generate HTML PoC')
		self.buttonpanel.add(self.buttonGeneratePoc)
		self.buttonGeneratePoc.addActionListener(self.actionListener)
		self.buttonSavePoc=JButton('Save PoC')
		self.buttonpanel.add(self.buttonSavePoc)
		self.buttonSavePoc.addActionListener(self.actionListener)
		self.buttonMoveUp=JButton('Move Up')
		self.buttonMoveDown=JButton('Move Down')
		self.buttonRemoveItem=JButton('Remove Item')
		self.buttonClear=JButton('Clear Table')
		self.panel2.add(self.buttonMoveUp)
		self.panel2.add(self.buttonMoveDown)
		self.panel2.add(self.buttonRemoveItem)
		self.panel2.add(self.buttonClear)
		self.buttonMoveUp.addActionListener(self.actionListener)
		self.buttonMoveDown.addActionListener(self.actionListener)
		self.buttonRemoveItem.addActionListener(self.actionListener)
		self.buttonClear.addActionListener(self.actionListener)
		self.messageHost=JTextField()
		self.messagePort=JTextField()
		self.messageProtocol=JTextField()
		self.buttonpanel.add(self.messageHost)
		self.buttonpanel.add(self.messagePort)
		self.buttonpanel.add(self.messageProtocol)

		self.mainsplit.setDividerLocation(300)
		self.split1_top.setDividerLocation(1000)
		self.split2_bottom.setDividerLocation(500)
		self.split3_bottom.setDividerLocation(1000)

		self.mainsplit.setLeftComponent(self.split1_top)
		self.mainsplit.setRightComponent(self.split2_bottom)
		self.split2_bottom.setLeftComponent(self.split3_bottom)
		self.split2_bottom.setRightComponent(self.buttonpanel)
		self.split1_top.setLeftComponent(self.scrollPane)
		self.split1_top.setRightComponent(self.panel2)
		self.split3_bottom.setLeftComponent(self.requestviewer.getComponent())
		self.split3_bottom.setRightComponent(self.pocviewer.getComponent())

		self.extender.callbacks.customizeUiComponent(self.mainsplit)
		self.extender.callbacks.customizeUiComponent(self.split1_top)
		self.extender.callbacks.customizeUiComponent(self.split2_bottom)
		self.extender.callbacks.customizeUiComponent(self.split3_bottom)
		self.extender.callbacks.customizeUiComponent(self.request_table)
		self.extender.callbacks.customizeUiComponent(self.scrollPane)
		self.extender.callbacks.customizeUiComponent(self.buttonpanel)
		self.extender.callbacks.customizeUiComponent(self.panel2)
		self.extender.callbacks.customizeUiComponent(self.buttonGeneratePoc)

		return self.mainsplit

class Table(JTable):
	def __init__(self, extender, data):
		self.extender = extender
		self.data=data
		self.setModel(AbstractTableModelclass(self.extender,self.data))
	def changeSelection(self, row, col, toggle, extend):
			self.selectedreq=self.data[row]
			self.extender.burptab.requestviewer.setMessage(self.selectedreq.getRequest(), True)
			self.service=self.selectedreq.getHttpService()
			self.extender.burptab.messageHost.setText(self.service.getHost())
			self.extender.burptab.messagePort.setText(str(self.service.getPort()))
			self.extender.burptab.messageProtocol.setText(self.service.getProtocol())
			JTable.changeSelection(self, row, col, toggle, extend)
	

class AbstractTableModelclass(AbstractTableModel):
	def __init__(self,extender,data):
		self.extender=extender
		self.columnNames=["S.No","Method","URL","Content Type"]
		self.data=data
	def getRowCount(self):
		try:
			return len(self.data)
		except:
			return 0

	def getColumnCount(self):
		return len(self.columnNames)

	def getColumnName(self, columnIndex):
		return self.columnNames[columnIndex]

	def getValueAt(self, rowIndex, columnIndex):
		self.rowentry = self.data[rowIndex]
		if columnIndex == 0:
			return rowIndex+1
		elif columnIndex == 1:
			return self.extender.helpers.analyzeRequest(self.rowentry).getMethod()
		elif columnIndex == 2:
			return self.extender.helpers.analyzeRequest(self.rowentry).getUrl()
		elif columnIndex == 3:
			return self.extender.helpers.analyzeRequest(self.rowentry).getContentType()
		else:
			return ""
	
	def getSelectedRow(self,rowIndex=0):
		return self.data[rowIndex]
	
	def addRow(self, message):
		rc=len(self.data)
		req=self.extender.callbacks.saveBuffersToTempFiles(message)
		self.data.append(req)
		self.extender.burptab.requestviewer.setMessage(self.extender.helpers.stringToBytes(""),False)

		self.fireTableRowsInserted(rc,rc)
	
	def removeRow(self, row):
		del self.data[row]
		self.fireTableRowsDeleted(row,row)

	def clearTable(self):
		del self.data[:]
		self.fireTableRowsDeleted(0,self.getRowCount())

class contextmenufactory(IContextMenuFactory):
	def __init__(self,extender):
		self.extender=extender
	def createMenuItems(self, invocation):
		self.invocation=invocation
		self.menuitems_list = []
		self.menuitems_list.append(JMenuItem("Send to CSRF PoC Generator",None,actionPerformed=lambda x: self.menuactiononclick(self.invocation)))
		if self.invocation.getInvocationContext() == self.invocation.CONTEXT_PROXY_HISTORY:
			self.extender.callbacks.printOutput('yes: invocation.CONTEXT_PROXY_HISTORY')
		else:
			self.extender.callbacks.printOutput(str(self.invocation.getInvocationContext()))

		return self.menuitems_list
	def menuactiononclick(self,inv):
		msgs=inv.getSelectedMessages()
		for r in msgs:
			self.extender.burptab.request_table.getModel().addRow(r)

class RequestData():
	def __init__(self,reqres):
		self.reqres=reqres

class BurpExtender(IBurpExtender):
	def	registerExtenderCallbacks(self, callbacks):
		self.callbacks=callbacks
		self.callbacks.setExtensionName("CSRF PoC Generator3")
		self.helpers=self.callbacks.getHelpers()
		self.stdout = PrintWriter(self.callbacks.getStdout(), True)
		self.stderr = PrintWriter(self.callbacks.getStderr(), True)
		self.stdout.println("Hello output")
		self.stderr.println("Hello errors")
		self.callbacks.issueAlert("Hello alerts")
		version=self.callbacks.getBurpVersion()
		print(version)
		self.stdout.println(version)
		#model=AbstractTableModelclass()
		self.contextmenu=contextmenufactory(self)
		self.callbacks.registerContextMenuFactory(self.contextmenu)
		self.burptab=burptab(self,'CSRF POC Generator Tab')
		self.callbacks.addSuiteTab(self.burptab)
