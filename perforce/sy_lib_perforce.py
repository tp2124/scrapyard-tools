__author__ = 'primm'
__doc__ = '''
Root level wrapper around p4Python API
'''

import P4 as perforce
import sys

class P4(object):
    def __init__(self, user, client, password):
        self._p4 = perforce.P4()
        self._p4.exception_level = 1
        # self._p4.api_level = 1
        
        self.user = user
        self.client = client
        self.password = password
        # self.port = port
        
        if self.user:
            self._p4.user = self.user
        elif self.client:
            self._p4.client = self.client
        elif self.password:
            self._p4.password = self.password
        # elif self.port:
        #     self._p4.port = self.port
        
        #Lets start talking to the server
        self._p4.connect()
        
        # if self.user and self.password:
            # #attempt to login as a specific user/password for a ticketed system
            # self._p4.run_login()
        
        if self.connected():
            self.p4info = self._p4.run("info")[0]

    def connected(self):
        """
        Returns True if a connection is open
        If initially closed, will attempt to open a connection and return True
        If connection initialization fails, returns False
        """
        if self._p4.connected():
            return True
        else:
            try:
                if not self._p4.connect():
                    #connection established
                    return True
                else:
                    #shouldn't get here
                    raise Exception('Got an undesirable place in p4.connected()')
                
            except perforce.P4Exception:
                #Could not establish a connection
                return False
            
    def open(self, file, fileType, changeID):
        # In Progress
    
        # Function that will check the file path to see if the server
        # needs to mark the files for add, checkout, etc.
        # Is incharge of adding the files to the desired changelistId
        # if fileType == 'text':
        if self.connected():
            changeList = self._p4.fetch_changelist(changeID)
            if not changeID =="":
                try:
                    changeFiles = changeList['Files']
                except:
                    #The changelist didn't have any files in it
                    changeFiles = []
                    changeList['Files'] = changeFiles
                if file not in changeFiles:
                    #File doesn't exist in the current changelist
                    result = self._p4.run('opened', file)
                    if not result:
                        #file is not opened by anyone
                        #Try to open the file for edit
                        result = self._p4.run('edit', file)
                        if not result:
                            #file didn't exist on the server
                            #Mark it for add
                            result = self._p4.run('add', '-c', changeID, file)
                    result = self._p4.run('reopen', '-c', changeID, file)
            else:
                result = self._p4.run('opened', file)
                result = self._p4.run('edit', file)
                if not result:
                    if not result:
                        result = self._p4.run('add', file)
                result = self._p4.run('reopen',  file) 
        # elif fileType == 'binary':
            # pass
        
        # elif fileType == 'unicode':
            # pass
            
    def runCmd(self, cmd, input):
        """
        Wrapper function to interface with P4 cmd calls
        """
        result = self._p4.run(cmd, input)
        return result
        
    def displayP4Info(self):
        """
        Prints current information about the perforce connection
        """
        for dict in self.p4info:
            for key in dict.keys():
                print key, '=', dict[key]
                
    def doesFileExistOnServer(self, filePath):
        """
        Function to return whether or not a file exists on the Perforce atm
        """
        if self.connected():
            result = self._p4.run('files', filePath)
            if result:
                return True
        return False
                
                
    def createChangelist(self, description):
        """
        Creates an empty changelist with the given description
        """
        import re
        if self.connected():
            changeID = ''
            pendingChanges = self._p4.run('changes', '-s', 'pending', '-u', os.environ['P4USER'])
            for change in pendingChanges:
                if change['desc'][:12] == description[:12]:
                    changeID = change['change']

            if not changeID:
                desc = {'Description': '%s' % description,
                        'Change': 'new',
                        }
                self._p4.input = desc
                result = self._p4.run('changelist', '-i')
                intIndex = re.search('\d', result[0])
                #Parsing the result message to find the changelist number
                for i in range(len(result[0]) - intIndex.start()):
                    searchResult = re.search('\d', result[0][intIndex.start() + i])
                    if searchResult:
                        changeID += result[0][intIndex.start() + i]
                    else:
                        break
        return int(changeID)
        

if __name__ == '__main__':
    pass

        