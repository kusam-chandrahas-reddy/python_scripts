#Creating Burp Extension for CSRF PoC Generator
from burp import IBurpExtender, IContextMenuFactory, ITab
from java.io import PrintWriter
from java.lang import RuntimeException
from java.awt import Panel
from javax.swing import JScrollPane, JTextArea, JLabel,JMenuItem

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
		self.label1.setBounds(x, y, 80, 20)
		self.panel.add(self.label1)
		self.payload = JTextArea()
		self.scrollpane = JScrollPane(self.payload)
		self.scrollpane.setBounds(x + 100, y, 200, 20)
		self.panel.add(self.scrollpane)
		return self.panel

#adding context menu
class contextmenufactory(IContextMenuFactory):
	def __init__(self,extender,callbacks):
		self.extender=extender
		self.callbacks=callbacks
	def createMenuItems(self, invocation):
		self.menuitems_list = []
		self.menuitems_list.append(JMenuItem("Send to CSRF PoC Generator",None,actionPerformed=lambda x,inv=invocation: self.menuaction(inv)))
		x=str(invocation.getToolFlag())
		a=str(self.callbacks.TOOL_PROXY)
		t=str(type(invocation.getToolFlag()))
		self.callbacks.printOutput(x)
		self.callbacks.printOutput(t)
		self.callbacks.printOutput(a)
		x=str(invocation.CONTEXT_PROXY_HISTORY)
		self.callbacks.printOutput('====')
		self.callbacks.printOutput(x)
		if invocation.getInvocationContext() == invocation.CONTEXT_PROXY_HISTORY:
			self.callbacks.printOutput('yes: invocation.CONTEXT_PROXY_HISTORY')
		else:

			self.callbacks.printOutput(str(invocation.getInvocationContext()))
			
		messages=invocation.getSelectedMessages()
		return self.menuitems_list
	def menuaction(self,inv):
		msg=inv.getSelectedMessages()
		self.extender.mytab.payload.setText('Payload from menu item')
		#Do something

class BurpExtender(IBurpExtender):
	
	#
	# implement IBurpExtender
	#
	
	def	registerExtenderCallbacks(self, callbacks):
		# set our extension name
		callbacks.setExtensionName("CSRF PoC Generator")
		helpers=callbacks.getHelpers()
		# obtain our output and error streams
		stdout = PrintWriter(callbacks.getStdout(), True)
		stderr = PrintWriter(callbacks.getStderr(), True)
		
		# write a message to our output stream
		stdout.println("Hello output")
		
		# write a message to our error stream
		stderr.println("Hello errors")
		
		# write a message to the Burp alerts tab
		callbacks.issueAlert("Hello alerts")

		version=callbacks.getBurpVersion()
		print(version)
		for i in version:
			print(i)
		stdout.println(version)

		self.contextmenu=contextmenufactory(self,callbacks)
		callbacks.registerContextMenuFactory(self.contextmenu)
		self.mytab=tab(self,'My Tab Name')
		callbacks.addSuiteTab(self.mytab)




	   # callbacks.unloadExtension()

		# throw an exception that will appear in our error stream
	   # raise RuntimeException("Hello exception")

