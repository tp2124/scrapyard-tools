__author__ = 'primm'
__doc__ = '''
This function is called at run time after maya is launched and the global variable is set from the
mel script createMenu.mel. createMenu.mel is called when maya is launched
from the Scrapyard launcher
'''
import maya.cmds as cmds


def doAnotherFunction():
    print 'got to another function'

def fillInScrapyardMenu():
    cmds.menuItem(l='someMenuItem', c=doAnotherFunction)
#    menuItem -label "My Fancy Command" -command "myFancyCommand";

print 'Python was imported'