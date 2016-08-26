__author__ = 'primm'
import os
import subprocess

directory = os.getcwd()
directory = directory.split('\\')
directory.pop()
directory.pop()
scrapyard_root = '\\'.join(directory) 

os.environ['PATH'] = scrapyard_root + '\\Tools\\Python27'
os.environ['SCRAPYARD_ROOT'] = scrapyard_root
os.environ['SY_ROOT'] = scrapyard_root
os.environ['MECHBRAWLER_TOOLS_DIR'] = scrapyard_root + '\\Tools'
os.environ['XBMLANGPATH'] = scrapyard_root + '\\Tools\\maya\\icons'
os.environ['SCRAPYARD_ASSEST_DIR'] = scrapyard_root + '\\Assests'
#Create me
#Getting list of scripts
allScriptPaths = []
for (path, dirs, files) in os.walk(os.environ['MECHBRAWLER_TOOLS_DIR'] + '\\Maya\\scripts'):
    allScriptPaths.append(path)
for (path, dirs, files) in os.walk(os.environ['MECHBRAWLER_TOOLS_DIR'] + '\\python'):
    allScriptPaths.append(path)
os.environ['PYTHONPATH'] = ';'.join(allScriptPaths) + ';' + os.environ['MECHBRAWLER_TOOLS_DIR'] + '\\Python27'
os.environ['MAYA_SCRIPT_PATH'] = ';'.join(allScriptPaths)
os.environ['MAYA_SHELF_PATH'] = os.environ['MECHBRAWLER_TOOLS_DIR'] + '\\Maya\\shelves'

#Checking for if in the lab or not
mayaExecutable = ''
try:
    mayaExecutable = '"%s\\bin\\maya.exe"' % (os.environ['MAYA_DIR'])
except KeyError:
    #If variable doesn't exist, we should be in the lab. Auto launching Maya
    #from lab machine path locations
    mayaExecutable = '"C:\\Program Files\\Autodesk\\Maya2011\\bin\\maya.exe"'

#Adding a variable to Maya launch to have Maya start with a .mel
#script in order to create the Scrapyard menu
mayaExecutable += ' -script %s\\maya\\createMenu.mel' % os.environ['MECHBRAWLER_TOOLS_DIR']
	
subprocess.call(mayaExecutable, shell=True)