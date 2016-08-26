__author__ = 'primm'
__doc__ = '''
This class is to create Scrapyard specific Perforce command calls
Debating giving the library to GamePipe/other teams
'''

from sy_lib_perforce import P4 as perforce
import os
from optparse import OptionParser
import sys
import xml.etree.ElementTree as ET

PERFORCE_PATH_TO_SY='//gamepipe/FinalGames/Fall2012/Scrapyard/Scrapyard_Main'

class P4(perforce):
    def __init__(self):
        perforce.__init__(self, os.environ['P4USER'], os.environ['P4CLIENT'], 'MechOut!')
        self.sy_RootDir = os.environ['SY_ROOT']

    def syncRoot(self):
        """
        Gets the latest revisions for the Assets and Tools directories
        """
        # This could take a while once the project gets rolling
        # if self._p4.connected():
        results = self.runCmd('sync', PERFORCE_PATH_TO_SY) 

    def syncDirectory(self, directory):
        """
        syncs whatever directory is passed in
        """ 
        results = self.runCmd('sync', directory)
        return results       
        
    def fetch_changelist(self, clNum):
        """
        Get description for specific changelist number
        """
        # if self.connected():
        # Getting more details about a specific changelist
        cl = self._p4.run('describe', clNum)
        print cl

    def getFilesInDefault(self):
        result = self._p4.run('opened', '-c', 'default')
        return result
        
    def testStuff(self):
        """

        """
        # if self.connected():
        #print self.getFilesInDefault()
        # result = self._p4.run('files', '//gamepipe/FinalGames/Fall2012/Scrapyard/Tools/python/EmailGenerator/lib_error_emailUpdate.py')
        # result = self._p4.run('opened', '//gamepipe/FinalGames/Fall2012/Scrapyard/Tools/python/EmailGenerator/sy_ToolsError.py')
        # result = self._p4.run('reopen', '-c', 9025, '//gamepipe/FinalGames/Fall2012/Scrapyard/Tools/python/EmailGenerator/lib_error_emailUpdate.py')
        # result = self._p4.run('files', '//gamepipe/FinalGames/somefile.py')
        # print 'result1: ', result
        # result = self._p4.run('add', '-c', 9025, '//gamepipe/FinalGames/Fall2012/Scrapyard/Assets/file.txt')
        # print 'result', result


def setP4EnvVar():
#Function to set local environment variables as determined via p4 file
    pathToP4File = os.environ['USERPROFILE'] + r'\.p4qt\ApplicationSettings.xml'
    tree = ET.parse(pathToP4File)

    parentNode = None
    for node in tree.getiterator():
        if node.attrib.get('varName') == 'RecentConnections':
            parentNode = node
    #Use index 0 because we only want the latest stored connection
    nodeWeWant = parentNode[0]
    loginInfo = nodeWeWant.text.split(',')
    username = loginInfo[1].strip()
    workspace = loginInfo[2].strip()
    #Save these datas to a file
    #P4USER
    fin = open(os.environ['SY_TOOLS_DIR'] + r'\Environment\P4USER', 'w')
    fin.write(username)
    fin.close()
    #P4CLIENT
    fin = open(os.environ['SY_TOOLS_DIR'] + r'\Environment\P4CLIENT', 'w')
    fin.write(workspace)
    fin.close()


def cmdSyncDirectories():
    """
    command line call to look at \\syncDirs.txt to find which directories to get latest
    """
    P4obj = P4()
    #Calling the update directories from commandline 
    #check updateDirectories.ini for which directories to update for
    updateSettingsPath = os.environ['SY_ROOT'] + '\\syncDirs.txt'
    if os.path.isfile(updateSettingsPath):
        FILE = open(updateSettingsPath, 'r')
        directories = set(FILE.read().splitlines())
        FILE.close()
        directories.discard('')
        for userGivenDirectory in directories:
            directory = userGivenDirectory.lstrip('.')
            directory = PERFORCE_PATH_TO_SY + directory + '/...'
            directory = directory.replace('\\','/')
            result = P4obj.syncDirectory(directory)
            print '\nFrom %s updated:' % userGivenDirectory
            for updatedFile in result:
                print '    %s' % updatedFile['clientFile']

    else:
        print "There is an error in finding \\\\syncDirs.txt. Update your root checkout on perforce."

if __name__ == '__main__':
    if not len(sys.argv) == 0:
        for arg in sys.argv:
            if arg == '-o':
                #Command line opening a file on perforce
                #
                # python sy_P4_Commands.py pathToFile *optional*ChangelistNumber P4USER P4CLIENT
                #
                openIndex = sys.argv.index(arg)
                P4obj = P4(user=os.environ['P4USER'], password='MechOut!', client=os.environ['P4CLIENT'])

                if sys.argv[openIndex + 2].isdigit():
                    P4obj.open(sys.argv[openIndex + 1],".txt",sys.argv[openIndex + 2])
                else:
                    P4obj.open(sys.argv[openIndex + 1],".txt","")
            
            if arg == 'sync':
                cmdSyncDirectories()

            #if a flag is passed, have it update the environment variable files
            if arg == 'writeP4Files':
                setP4EnvVar()