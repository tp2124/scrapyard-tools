__author__ = 'primm'
import os
import subprocess
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def launchMaya():
	mayaExecutable = ''
	try:
	    mayaExecutable = '"%s\\bin\\maya.exe"' % (os.environ['MAYA_DIR'])
	except KeyError:
	    #If variable doesn't exist, we should be in the lab. Auto launching Maya
	    #from lab machine path locations
	    mayaExecutable = '"C:\\Program Files\\Autodesk\\Maya2011\\bin\\maya.exe"'

	#Adding a variable to Maya launch to have Maya start with a .mel
	#script in order to create the Scrapyard menu
	mayaExecutable += ' -script %s\\maya\\createMenu.mel' % os.environ['SY_TOOLS_DIR']
		
	subprocess.call(mayaExecutable, shell=True)

if __name__ == "__main__":
	launchMaya()
