__author__ = 'primm'
__doc__ = '''
Object reset function to be used anywhere. 
'''

import maya.cmds as cmds
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def zeroObject(moveGeo = False):
    if moveGeo:
        selectedMeshes = cmds.ls(sl = True)
        #for moving geometry as well
        for mesh in selectedMeshes:
            cmds.move( 0, 0, 0, mesh, absolute = True)
            cmds.makeIdentity(apply = True, t = True, r = True, s = True, n = 0)
            cmds.xform(absolute = True, worldSpace = True, piv = (0, 0, 0))
            cmds.delete(constructionHistory = True)
            
	#Changing the Transform to the origin
    cmds.xform(absolute = True, worldSpace = True, piv = (0, 0, 0))
    cmds.makeIdentity(apply = True, t = True, r = True, s = True, n = 0)
    cmds.delete(constructionHistory = True)
    