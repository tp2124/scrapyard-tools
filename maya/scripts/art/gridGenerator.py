__author__ = 'primm'

import maya.cmds as cmds

maxSize = 2048
divisions = maxSize/4
_spacing = 2048


cmds.grid(size=maxSize, spacing=_spacing, d=divisions)