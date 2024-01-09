#Creating Burp Extension for CSRF PoC Generator
from burp import IBurpExtender, IContextMenuFactory, ITab, ITextEditor
from java.io import PrintWriter
from java.lang import RuntimeException
from java.awt import Panel
from javax.swing import JScrollPane, JTextArea, JLabel,JMenuItem


class texteditor(ITextEditor):
	def __init__(self,extender):
		pass
	
#creating a new tab in Burp Suite
class tab(ITab):
	def __init__(self,extender,name):
		self.name=name
		self.extender=extender
	def getTabCaption(self):
		return self.name
	def getUiComponent(self):
		x=10
		self.name='asdf'
		# Returning instance of the panel as in burp's docs
		x = 10  # panel padding
		y = 10  # panel padding
		self.panel = Panel()
		self.panel.setLayout(None)
		self.label1 = JLabel("Payload Value")
		self.label1.setBounds(x, y, 120, 20)
		self.panel.add(self.label1)
		self.payload = JTextArea()
		self.scrollpane = JScrollPane(self.payload)
		self.scrollpane.setBounds(x, y+40, 1000, 400)
		self.panel.add(self.scrollpane)
		return self.panel

#adding context menu
class contextmenufactory(IContextMenuFactory):
	def __init__(self,extender):
		self.extender=extender
	def createMenuItems(self, invocation):
		self.invocation=invocation
		self.menuitems_list = []
		self.menuitems_list.append(JMenuItem("Send to CSRF PoC Generator",None,actionPerformed=lambda x: self.menuaction(invocation)))
		x=str(invocation.getToolFlag())
		a=str(self.extender.callbacks.TOOL_PROXY)
		t=str(type(invocation.getToolFlag()))
		self.extender.callbacks.printOutput(x)
		self.extender.callbacks.printOutput(t)
		self.extender.callbacks.printOutput(a)
		x=str(invocation.CONTEXT_PROXY_HISTORY)
		self.extender.callbacks.printOutput('====')
		self.extender.callbacks.printOutput(x)
		if invocation.getInvocationContext() == invocation.CONTEXT_PROXY_HISTORY:
			self.extender.callbacks.printOutput('yes: invocation.CONTEXT_PROXY_HISTORY')
		else:

			self.extender.callbacks.printOutput(str(invocation.getInvocationContext()))
			
		messages=invocation.getSelectedMessages()
		return self.menuitems_list
	def menuaction(self,inv):
		msg=inv.getSelectedMessages()
		req=msg[0].getRequest().tolist()
		reqdata=''.join(map(chr,req))
		self.extender.mytab.payload.setText(reqdata)
		
		
		#Do something

class BurpExtender(IBurpExtender):
	
	#
	# implement IBurpExtender
	#
	
	def	registerExtenderCallbacks(self, callbacks):
		self.callbacks=callbacks
		# set our extension name
		self.callbacks.setExtensionName("CSRF PoC Generator")
		helpers=self.callbacks.getHelpers()
		# obtain our output and error streams
		stdout = PrintWriter(self.callbacks.getStdout(), True)
		stderr = PrintWriter(self.callbacks.getStderr(), True)
		
		# write a message to our output stream
		stdout.println("Hello output")
		
		# write a message to our error stream
		stderr.println("Hello errors")
		
		# write a message to the Burp alerts tab
		self.callbacks.issueAlert("Hello alerts")

		version=self.callbacks.getBurpVersion()
		print(version)
		for i in version:
			print(i)
		stdout.println(version)

		self.contextmenu=contextmenufactory(self)
		self.callbacks.registerContextMenuFactory(self.contextmenu)
		self.mytab=tab(self,'My Tab Name')
		self.callbacks.addSuiteTab(self.mytab)




	   # callbacks.unloadExtension()

		# throw an exception that will appear in our error stream
	   # raise RuntimeException("Hello exception")

