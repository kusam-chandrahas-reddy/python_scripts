from burp import IBurpExtender, IContextMenuFactory
from javax.swing import JMenuItem, JDialog, JFrame, JButton, JPanel, JLabel, JSplitPane
from java.awt import GridBagLayout, GridBagConstraints, Insets
from java.lang import Double

class BurpExtender(IBurpExtender, IContextMenuFactory):
	def registerExtenderCallbacks(self,callbacks):
		self.callbacks=callbacks
		callbacks.setExtensionName('Clickjacking PoC Creator')
		self.helpers=callbacks.getHelpers()
		callbacks.registerContextMenuFactory(self)
		self.poc="""
<html>
<head><title>Clickjacking PoC</title></head>
<body>
<h4>Clickjacking PoC</h4>
<iframe src="{}"></iframe>
</body>
</html>
"""
	def createMenuItems(self, invocation):
		self.invocation=invocation
		self.menuItems=[]
		self.menuItems.append(JMenuItem('Clickjacking PoC',None,actionPerformed=lambda x: self.createPoc()))
		return self.menuItems
	def createPoc(self):
		msgs=self.invocation.getSelectedMessages()
		for m in msgs:
			req=self.helpers.analyzeRequest(m)
			self.createpop1(str(req.getUrl()))
			break
			pass
	def createpop1(self,url):
		f1=JFrame('My Frame')
		self.dialog1=JDialog(f1,'Clickjacking Proof Of Concept2')
		l1=JLabel('Clickjacking PoC')
		l2=JLabel(url)
		t=self.callbacks.createTextEditor()
		t.setText(self.poc.format(str(url)))
		save=JButton('Save')
		generate=JButton('Generate')
		p=JPanel()
		sp=JSplitPane(JSplitPane.VERTICAL_SPLIT)
		sp.setLeftComponent(t.getComponent())
		p2=JPanel()
		p2.add(save)
		p2.add(generate)
		sp.setRightComponent(p2)
		sp.setDividerLocation(Double("0.7").doubleValue())
		self.dialog1.add(sp)
		self.dialog1.setBounds(400,200,800,600)
		self.dialog1.setVisible(True)
		self.callbacks.customizeUiComponent(f1)
		self.callbacks.customizeUiComponent(sp)
		self.callbacks.customizeUiComponent(p2)
		self.callbacks.customizeUiComponent(self.dialog1)
		self.callbacks.customizeUiComponent(l1)
		self.callbacks.customizeUiComponent(l2)
		self.callbacks.customizeUiComponent(p)
		self.callbacks.customizeUiComponent(save)
		self.callbacks.customizeUiComponent(generate)

	def createpop(self,url):
		f1=JFrame('My Frame')
		self.dialog=JDialog(f1,'Clickjacking Proof Of Concept1')
		l1=JLabel('Clickjacking PoC')
		l2=JLabel(url)
		t=self.callbacks.createTextEditor()
		save=JButton('Save')
		generate=JButton('Generate')
		p=JPanel()
		gl=GridBagLayout()
		gl.columnWidths = [10, 0, 0, 0]
		gl.rowHeights = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		gl.columnWeights = [0.0, 1.0, 0.0, Double.MIN_VALUE]
		gl.rowWeights = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,Double.MIN_VALUE]
		p.setLayout(gl)
		gc=GridBagConstraints()
		
		gc.fill=GridBagConstraints.HORIZONTAL		
		gc.gridx=0
		gc.gridy=0
		p.add(l1,gc)

		gc.fill=GridBagConstraints.HORIZONTAL
		gc.gridx=0
		gc.gridy=1
		p.add(l2,gc)
		
		gc.fill=GridBagConstraints.HORIZONTAL
		gc.gridx=0
		gc.gridy=2
		gc.gridwidth=4
		#gc.gridheight=4
		gc.ipady=200
		p.add(t.getComponent(),gc)
		
		gc.fill=GridBagConstraints.HORIZONTAL
		gc.ipady=0
		gc.anchor = GridBagConstraints.PAGE_END
		gc.gridwidth=1
		
		gc.gridx=0
		gc.gridy=7
		p.add(save,gc)
		
		gc.fill=GridBagConstraints.HORIZONTAL
		gc.insets=Insets(10,0,0,0)
		gc.gridwidth=1
		gc.gridx=2
		gc.gridy=7
		p.add(generate,gc)
		
		self.dialog.add(p)
		self.dialog.setBounds(400,200,800,600)
		self.dialog.setVisible(True)
		self.callbacks.customizeUiComponent(f1)
		self.callbacks.customizeUiComponent(self.dialog)
		self.callbacks.customizeUiComponent(l1)
		self.callbacks.customizeUiComponent(l2)
		self.callbacks.customizeUiComponent(p)
		self.callbacks.customizeUiComponent(save)
		self.callbacks.customizeUiComponent(generate)




	def createPopupWindow(self,url):
		f=JFrame('My Frame')
		self.d=JDialog(f,'Clickjacking Proof Of Concept')
#		f2=JFrame('Frame 2')
		l1=JLabel('Clickjacking PoC')
		l2=JLabel(url)
		t=self.callbacks.createTextEditor()
		#self.d.add(t.getComponent())
		p=JPanel()
#		f2.getContentPane().setLayout(None)
		p.setLayout(None)
		p.add(l1)
		l1.setBounds(10,10,200,20)
		p.add(l2)
		#l2.setBounds(10,700,200,20)
#		p2=JPanel()
		t.getComponent().setBounds(10,40,650,350)
		p.add(t.getComponent())
		save=JButton('Save')
		generate=JButton('Generate')
		l2.setBounds(20,400,300,20)
		save.setBounds(350,400,100,30)
		generate.setBounds(500,400,100,30)
		p.add(save)
		p.add(generate)

#		f2.setVisible(True)
#		f2.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
		#p.add(p2)
#		f2.add(p)
		self.d.add(p)
		#self.d.add(l1)
		#self.d.add(l2)
		
		self.d.setBounds(400,200,800,600)
		#self.d.setSize(800,600)
		self.d.setVisible(True)
		self.callbacks.customizeUiComponent(f)
		self.callbacks.customizeUiComponent(self.d)
		self.callbacks.customizeUiComponent(l1)
		self.callbacks.customizeUiComponent(l2)
		self.callbacks.customizeUiComponent(p)
		return 
	
		self.f=JFrame('Clickjacking')
		b=JButton('Create')
		b.actionListener(self)
		p=JPanel()
		p.add(b)
		self.f.add(p)
		self.f.setSize(400,400)
		self.f.show()
	def actionPerformed(self, e):
		cmd=e.getActionCommand()
		pass








