from PyQt4 import QtGui, QtCore
from assetDirectoriesWidget import AssetDirGeneratorWidget

app = None
win = None

def runStandalone():
    import sys
    from standAlone import AssetDirGeneratorWidget as StandAloneWidget
    global app
    global win
    app = QtGui.QApplication(sys.argv)
    win = StandAloneWidget()
    win.show()
    app.exec_()

def runMaya():
    plugin = 'ThreadedQtPlugin.py'
    if not cmds.pluginInfo(plugin, Query = True, loaded = True):
        #if Qt isn't loaded, fix that
        cmds.loadPlugin(plugin)
    app = QtGui.qApp
    app.connect(app, QtCore.SIGNAL('lastWindowClosed()'),
                app, QtCore.SLOT('quit()'))
    win = AssetDirGeneratorWidget()
    win.show()
        
def run():
    #figure out if being run in standAlone or Maya
    isMaya = False
    try:
        import maya.cmds as cmds
        isMaya = True
    except ImportError:
        isMaya = False

    if isMaya:
        runMaya()
    else:
        runStandalone()

if __name__ == '__main__':
    run()
