__author__ = 'primm'
__doc__ = '''
Allows artists to wipe transform data in a custom manner. 
'''

import maya.cmds as cmds
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def cleanGeometry():
    result = cmds.confirmDialog( title='Confirm', 
                        message='About to move the following selected meshes geometry, as well as their transforms, to the origin:\n   %s' % stringOfMeshes, 
                        button=['Move Geometry and Zero Transform','Cancel'], 
                        defaultButton='Move and Zero Transform')