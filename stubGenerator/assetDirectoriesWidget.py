__doc__ ="""
This is a generic GUI that will be used by multiple applications
Do not put application specific code in this file
Create a new file to inherit it. See standAlone.py for example
"""

from PyQt4 import QtGui, QtCore
import os
import sys
##########Importing Notifier lib
#sys.path.append(os.getcwd() + '\\..\\emailDecorator')
from lib_error_emailUpdate import emailNotifyer

class AssetDirGeneratorWidget(QtGui.QWidget):
    def __init__(self, *args):
        super(AssetDirGeneratorWidget, self).__init__()
        #General Window stuff
        self.move(300, 200)
        self.setWindowTitle('Create Asset Directories/Data')
        self.existingAssets = []
        self.getExistingAssets()
        self.existingTypes = []
        self.getExistingTypes()
        
        #Create more widgets
        self.vMainLayout = QtGui.QVBoxLayout()
        self.vTypeLayout = QtGui.QVBoxLayout()
        self.vNameLayout = QtGui.QVBoxLayout()
        # self.vFileLayout = QtGui.QVBoxLayout()
        # self.hFileTextLayout = QtGui.QHBoxLayout()
        self.hButtonLayout = QtGui.QHBoxLayout()
        self.typeLabel = QtGui.QLabel('Asset Types')
        self.w_typeName = QtGui.QComboBox()
        self.w_typeNameText = QtGui.QLineEdit('Please type in new Type names here')
        self.w_typeSpace = QtGui.QLabel('')
        self.assetLabel = QtGui.QLabel('Asset Names')
        self.w_assetName = QtGui.QComboBox()
        self.w_assetNameText = QtGui.QLineEdit('Please type in new Asset names here')
        self.w_assetSpace = QtGui.QLabel('')
        self.createStubsButton = QtGui.QPushButton('Create Stubs')
        self.cancelButton = QtGui.QPushButton('Cancel')
        self.w_buttonSpace = QtGui.QLabel('')
        # self.fileLabel = QtGui.QLabel('Choose your File')
        # self.w_fileText= QtGui.QLineEdit('Choose a file to Upload')
        # self.w_fileButton = QtGui.QPushButton('Browse')
        # self.w_fileSpace = QtGui.QLabel('')
        
        #Adding data to any of the widgets
        self.w_assetName.insertItems(0, self.existingAssets)
        self.w_assetName.insertItem(0, '---New Asset---')
        self.w_assetName.setCurrentIndex(0)
        
        self.w_typeName.insertItems(0, self.existingTypes)
        self.w_typeName.insertItem(0, '---New Type---')
        self.w_typeName.setCurrentIndex(0)
        
        #Adding widgets to layout
        self.vTypeLayout.addWidget(self.typeLabel)
        self.vTypeLayout.addWidget(self.w_typeName)
        self.vTypeLayout.addWidget(self.w_typeNameText)
        self.vTypeLayout.addWidget(self.w_typeSpace)
        
        self.vNameLayout.addWidget(self.assetLabel)
        self.vNameLayout.addWidget(self.w_assetName)
        self.vNameLayout.addWidget(self.w_assetNameText)
        self.vNameLayout.addWidget(self.w_assetSpace)
        
        self.hButtonLayout.addWidget(self.createStubsButton)
        self.hButtonLayout.addWidget(self.cancelButton)
        
        # self.vFileLayout.addWidget(self.fileLabel)
        # self.hFileTextLayout.addWidget(self.w_fileText)
        # self.hFileTextLayout.addWidget(self.w_fileButton)
        # self.vFileLayout.addLayout(self.hFileTextLayout)
        # self.vFileLayout.addWidget(self.w_fileSpace)
        
        self.vMainLayout.addLayout(self.vTypeLayout)
        self.vMainLayout.addLayout(self.vNameLayout)
        # self.vMainLayout.addLayout(self.vFileLayout)
        self.vMainLayout.addLayout(self.hButtonLayout)
        self.setLayout(self.vMainLayout)
        
        #Pair signals with slots
        self.connect(self.createStubsButton,
                    QtCore.SIGNAL('clicked()'),
                    self.makeDirectories)
                    
        self.connect(self.cancelButton,
                    QtCore.SIGNAL('clicked()'),
                    self.exit)
                    
        self.connect(self.w_typeName,
                    QtCore.SIGNAL('currentIndexChanged(const QString&)'),
                    self.updateAssetNames)
        '''
        self.connect(self.w_fileButton,
                    QtCore.SIGNAL('clicked()'),
                    self.getFileDialog)
        '''
        self.setMinimumWidth(300)
        #Show me
        self.show()
        
        
    def getFileDialog(self):
        #QFileDialog
        pass
        
    def exit(self):
        self.close()
        
    @emailNotifyer
    def updateAssetNames(self):
        self.existingAssets = []
        newType = str(self.w_typeName.currentText())
        self.w_assetName.clear()
        if newType == '---New Type---':
            self.getExistingAssets()
        else:
            #A specific type is chosen
            for root, dirs, files in os.walk(self.getAssetDirPath() + 'Source\\' + newType):
                if root.split('\\')[-1] == newType:
                    self.existingAssets = dirs
                    break

        self.w_assetName.insertItems(0, self.existingAssets)
        self.w_assetName.insertItem(0, '---New Asset---')
        self.w_assetName.setCurrentIndex(0)    
        
    def getAssetDirPath(self):
        myCurrentPath = os.getcwd() + '\\'
        return myCurrentPath + r'..\..\..\Assets\\'
    
    @emailNotifyer
    def makeDirectories(self):
        assetPath = self.getAssetDirPath()
        
        type = str(self.w_typeName.currentText())
        name = str(self.w_assetName.currentText())
        
        if type == '---New Type---':
            type = str(self.w_typeNameText.text())
            if type == 'Please type in new Type names here':
                #User chose New Type, but did not input any text
                return
                
        if name == '---New Asset---' and name != 'Should not stub an already created Asset':
            name = str(self.w_assetNameText.text())
            if name == 'Please type in new Asset names here':
                #User chose New Asset, but did not input any text
                return
        else:
            self.w_assetNameText.insert('Should not stub an already created Asset')
        
        #Source Dirs
        screenshotsDir = assetPath + r'Source\%s\%s\References' % (type, name)
        meshesDir = assetPath + r'Source\%s\%s\Meshes' % (type, name)
        mapsDir = assetPath + r'Source\%s\%s\Maps' % (type, name)
        moviesDir = assetPath + r'Source\%s\%s\Animations' % (type, name)
        
        #Export Dir
        exportSMDir = assetPath + r'Export\%s\%s\StaticMesh' % (type, name)
        exportAnimDir = assetPath + r'Export\%s\%s\Animations' % (type, name)
        exportSkeleDir = assetPath + r'Export\%s\%s\SkeletalMesh' % (type, name)

        try:
            os.makedirs(screenshotsDir)
        except WindowsError:
            print 'Directory already exist'
        try:
            os.makedirs(meshesDir)
        except WindowsError:
            print 'Directory already exist'
        try:
            os.makedirs(mapsDir)
        except WindowsError:
            print 'Directory already exist'
        try:
            os.makedirs(moviesDir)
        except WindowsError:
            print 'Directory already exist'
        try:
            os.makedirs(exportSMDir)
        except WindowsError:
            print 'Directory already exist'
        try:
            os.makedirs(exportAnimDir)
        except WindowsError:
            print 'Directory already exist'
        try:
            os.makedirs(exportSkeleDir)
        except WindowsError:
            print 'Directory already exist'
        self.close()
            
    def getExistingAssets(self):
        assetPath = self.getAssetDirPath()
        for root, dirs, files in os.walk(assetPath + 'Source'):
            if 'Maps' in dirs and 'Meshes' in dirs:
                self.existingAssets.append(root.split('\\')[-1])

    def getExistingTypes(self):
        assetPath = self.getAssetDirPath()
        for root, dirs, files in os.walk(assetPath + 'Source'):
            if root.split('\\')[-1] == 'Source':
                self.existingTypes = dirs
    