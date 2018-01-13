import sys
from PyQt4 import QtGui, QtCore
import os,glob,shutil




class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(0,0,500,300)
		self.setWindowTitle("usbtousb")
		self.setWindowIcon(QtGui.QIcon('logo.png'))

		extractAction = QtGui.QAction("&NOW QUIT",self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip("Leave the app")
		extractAction.triggered.connect(self.close_application)


		openEditor = QtGui.QAction("&Editor",self)
		openEditor.setShortcut("Ctrl+E")
		openEditor.setStatusTip('Open Editor')
		openEditor.triggered.connect(self.editor)

		openFile = QtGui.QAction("&Open File",self)
		openFile.setShortcut("Ctrl+O")
		openFile.setStatusTip('Open File')
		openFile.triggered.connect(self.file_open)
		self.statusBar()

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(extractAction)
		fileMenu.addAction(openFile)


		editorMenu = mainMenu.addMenu("&Editor")
		editorMenu.addAction(openEditor)

		self.home()




	def home(self):
		btn = QtGui.QPushButton("Quit", self)
		#btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		btn.clicked.connect(self.close_application)

		#btn.resize(100,100)
		btn.resize(btn.minimumSizeHint())
		btn.move(100,100)

		extractAction = QtGui.QAction(QtGui.QIcon('logo.png'),'flee',self)
		extractAction.triggered.connect(self.close_application)
		self.toolBar = self.addToolBar("Extraction")
		self.toolBar.addAction(extractAction)

		fontChoice = QtGui.QAction('Fonte',self)
		fontChoice.triggered.connect(self.font_choice)
		#self.toolBar = self.addToolBar("Font")
		self.toolBar.addAction(fontChoice)

		# color = QtGui.QColor(0,0,0)
		# fontColor = QtGui.QAction('font bf color',self)
		# fontColor.triggered.connect(self.color_picker)

		# self.toolBar.addAction(fontColor)



		checkBox = QtGui.QCheckBox("Enlarge",self)
		checkBox.move(200,200)
		#checkBox.toggle()
		checkBox.stateChanged.connect(self.enlarge_window)

		self.progress = QtGui.QProgressBar(self)
		self.progress.setGeometry(200,80,250,20)

		self.btn = QtGui.QPushButton("USB Copy AtB",self)
		self.btn.move(200,120)
		self.btn.resize(150,30)
		self.btn.clicked.connect(self.copyscript)
		
		self.btn = QtGui.QPushButton("USB Copy BtA",self)
		self.btn.move(200,150)
		self.btn.resize(150,30)
		self.btn.clicked.connect(self.copyscriptba)

		self.btn = QtGui.QPushButton("FTP Copy",self)
		self.btn.move(200,180)
		self.btn.resize(150,30)
		self.btn.clicked.connect(self.copyscriptftp)

		self.btn = QtGui.QPushButton("Copy Files To A",self)
		self.btn.move(200,210)
		self.btn.resize(150,30)
		self.btn.clicked.connect(self.uploadb)
		
		self.btn = QtGui.QPushButton("Copy Files To B",self)
		self.btn.move(200,240)
		self.btn.resize(150,30)
		self.btn.clicked.connect(self.upload)
		
		self.btn = QtGui.QPushButton("List Drives",self)
		self.btn.move(200,270)
		self.btn.resize(150,30)
		self.btn.clicked.connect(self.listd)

		print(self.style().objectName())
		self.styleChoice = QtGui.QLabel("Windows Vista",self)

		comboBox = QtGui.QComboBox(self)
		comboBox.addItem("motif")
		comboBox.addItem("Windows")
		comboBox.addItem("cde")
		comboBox.move(50,250)
		self.styleChoice.move(50,150)
		comboBox.activated[str].connect(self.style_choice)

		# cal = QtGui.QCalendarWidget(self)
		# cal.move(500,200)
		# cal.resize(200,200)


		self.show()

	# def color_picker(self):
	# 	color = QtGui.QColorDialog.getColor()
	# 	self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())

	def upload_blob(bucket_name, source_file_name, destination_blob_name):
	    """Uploads a file to the bucket."""
	    storage_client = storage.Client()
	    bucket = storage_client.get_bucket(bucket_name)
	    blob = bucket.blob(destination_blob_name)

	    blob.upload_from_filename(source_file_name)

	    print('File {} uploaded to {}.'.format(
	        source_file_name,
	        destination_blob_name))


	def  file_open(self):
		name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
		file = open(name,'r')
		self.editor()

		with file:
			text = file.read()
			self.textEdit.setText(text)


	def font_choice(self):
		font, valid = QtGui.QFontDialog.getFont()
		if valid:
			self.styleChoice.setFont(font)

	def editor(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)

	def style_choice(self,text):
		self.styleChoice.setText(text)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))


	def upload(self):
		self.completed = 0

		name = QtGui.QFileDialog.getOpenFileNames(self, 'Open File')

		drive_list=[]
		drive_list=self.drives()

		for drives in drive_list:
			print drives
		destination = "/media/pi/"+drive_list[1]+"/"

		for names in name:
			print("Copying"+names)
			self.completed+=100
			os.system('cp -r '+ "'"+str(names)+"' " + destination)
			print("Copied")
			
	def listd(self):
		

		
		drive_list=self.drives()

		for i,drives in enumerate(drive_list):
			if(i==0):
				print 'A = '+drives
			if(i==1):
				print 'B = '+drives
			if(i==2):
				print 'C = '+drives
			
			
	def uploadb(self):
		self.completed = 0

		name = QtGui.QFileDialog.getOpenFileNames(self, 'Open File')

		drive_list=[]
		drive_list=self.drives()

		for drives in drive_list:
			print drives
		destination = "/media/pi/"+drive_list[0]+"/"

		for names in name:
			print("Copying"+names)
			self.completed+=100
			os.system('cp -r '+ "'"+str(names)+"' " + destination)
			print("Copied")


	def drives(self):

		while True:
			drive_list = os.listdir('/media/pi/' )
			if(len(drive_list)>=3):
				break
			else:
				print("Waiting for pendrives to connect"+str(len(drive_list)))

		return drive_list

	def copyscript(self):
		self.completed = 0

		

		while True:
			drive_list = os.listdir('/media/pi/.' )
			if(len(drive_list)>=3):
				break
			else:
			    for i,drives in enumerate(drive_list):
			        print str(i)+drives
                print("Waiting for pendrives to connect"+str(len(drive_list)))

		for i,drives in enumerate(drive_list):
			print str(i)+drives
		destination = "/media/pi/"+drive_list[1]+"/"

		usba=[]
		usbb=[]

		for i, drive_name in enumerate( drive_list ):
	
			for j, files_path in enumerate( glob.glob( '/media/pi/'+drive_name+'/*' ) ):
				
					if(i==0):
						usba.append(files_path)
					if(i==1):
						usbb.append(files_path)
					print(i, files_path )
		print("asd")
		for i, names in enumerate(usba):
			print("Copying"+names)
			self.completed+=100/len(usba)
			self.progress.setValue(self.completed)
			os.system('cp -r '+ "'"+names+"' " + destination)
			print("Copied")

	def copyscriptba(self):
		self.completed = 0

		

		while True:
			drive_list = os.listdir('/media/pi/.' )
			if(len(drive_list)>=3):
				break
			else:
			    for i,drives in enumerate(drive_list):
			        print str(i)+drives
                print("Waiting for pendrives to connect"+str(len(drive_list)))

		for i,drives in enumerate(drive_list):
			print str(i)+drives
		destination = "/media/pi/"+drive_list[0]+"/"

		usba=[]
		usbb=[]

		for i, drive_name in enumerate( drive_list ):
	
			for j, files_path in enumerate( glob.glob( '/media/pi/'+drive_name+'/*' ) ):
				
					if(i==0):
						usba.append(files_path)
					if(i==1):
						usbb.append(files_path)
					print(i, files_path )
		print("asd")
		for i, names in enumerate(usbb):
			print("Copying"+names)
			self.completed+=100/len(usbb)
			self.progress.setValue(self.completed)
			os.system('cp -r '+ "'"+names+"' " + destination)
			print("Copied")
	

	
	def copyscriptftp(self):
		self.completed = 0

		

		
		drive_list = os.listdir('/media/pi/.' )
			

		destination = "/media/ftp/"

		usba=[]
		usbb=[]

		for i, drive_name in enumerate( drive_list ):
	
			for j, files_path in enumerate( glob.glob( '/media/pi/'+drive_name+'/*' ) ):
				
					if(i==0):
						usba.append(files_path)
					if(i==1):
						usbb.append(files_path)
					print(i, files_path )

		for i, names in enumerate(usba):
			print("Copying"+names)
			self.completed+=0.0001
			os.system('cp -r '+ "'"+names+"' " + destination)
			self.progress.setValue(self.completed)
		for i, names in enumerate(usbb):
			print("Copying"+names)
			self.completed+=0.0001
			os.system('cp -r '+ "'"+names+"' " + destination)
			self.progress.setValue(self.completed)
			print("Copied")

			

	def editor(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)

	def enlarge_window(self,state):
		if state == QtCore.Qt.Checked:
			self.setGeometry(50,50,1000,600)
		else:
			self.setGeometry(50,50,500,300)

	def close_application(self):
		choice = QtGui.QMessageBox.question(self, "Sure!","Made in upes with <3",
												QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			print("Extractinggg")
			sys.exit()

		else:
			pass

	def closeEvent(self, event):
		event.ignore()
		self.close_application()

def run():
	app = QtGui.QApplication(sys.argv) # to call from command line

	GUI = Window()

	sys.exit(app.exec_())


run()