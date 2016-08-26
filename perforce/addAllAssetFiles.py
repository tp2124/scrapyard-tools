__author__ = 'primm'
__doc__ = '''
Function to help with uploading of hitbox data.
'''

import os
import sy_P4_commands as perforce
import sys
#Importing Notifier lib
sys.path.append(os.getcwd() + '\\..\\emailDecorator')
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def findNewFilesAndUpload():
    #This function is more of a wrapper in order to use the decorator
    #in order to create crash reports
    listOfAllAssetFiles = []
    print '\nSearching in directories:\n\t', assetRoot, '\n\t', jsonHitboxRoot
    for root, dirs, files in os.walk(assetRoot):
        for file in files:
            root = root.replace('\\','/')
            fullPath = root + '/' + file
            if not p4.doesFileExistOnServer(fullPath):
                #If file isn't on P4, add to list
                listOfAllAssetFiles.append(fullPath)
    
    for root, dirs, files in os.walk(jsonHitboxRoot):
        for file in files:
            root = root.replace('\\','/')
            fullPath = root + '/' + file
            if not p4.doesFileExistOnServer(fullPath):
                #If file isn't on P4, add to list
                listOfAllAssetFiles.append(fullPath)
    
    #If any new files are found, create a new changelist, and mark the files for add
    #on that new changelist
    if listOfAllAssetFiles:
        print '\nMarking files for add:'
        changeID = p4.createChangelist('Auto_Adding_Assets: %s' % p4.p4info['userName'])
        for file in listOfAllAssetFiles:
            p4.open(file, 'text', changeID)
            print '\t%s' % file.replace(p4.sy_RootDir, '')

#Get directories to search
if __name__ == '__main__':
    username = raw_input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nScrapyard P4 Login\nP4 Username:')
    p4 = perforce.P4(user = username, password = 'MechOut!')
    sy_Root = p4.sy_RootDir.replace('\\', '/')
    assetRoot = sy_Root + 'Assets'
    jsonHitboxRoot = sy_Root + 'Jsons\\HitBoxes'

    findNewFilesAndUpload()

