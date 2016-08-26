__author__ = 'primm'
__doc__ = '''
Set the camera to the location that it will be while playing the game. 
'''

'''
TODO: This should go into sy_utils once paths are good
'''

import maya.cmds as cmds
import math

def generateGameCamera():
    xOffset = 500
    yOffset = 150
    camName = cmds.camera(n='Game_Camera', hfv=90)
    cmds.xform(ro=(-(90-(math.atan(xOffset/yOffset)/math.pi) * 180) , 90, 0), s=(30, 30, 30), t=(xOffset, yOffset, 0))
    