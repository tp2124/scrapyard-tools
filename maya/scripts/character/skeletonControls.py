import maya.cmds as cmds
import maya.mel as mel
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def createMayaBox(jointName, parentJointName, amIRoot):
    #print 'Trying to create controlBox, jointName: %s\n   parentJointName: %s\n amIRoot: %s' % (jointName, parentJointName, amIRoot)
    cmds.select(jointName)
    parentJnt = cmds.listRelatives(jointName, p = True)
    jntTrans = cmds.xform(q = True, translation = True, ws = True)
    jntRot = cmds.xform(q = True, rotation = True, ws = True)
    cmds.makeIdentity(apply = True, jo = True)
    controlName = 'Control_%s' % jointName
    if jointName.lower() == 'root':
        #special shape for the root
        newCurve = cmds.circle(n = controlName, nr = (0,1,0), r = 30)[0]
    else:
        #default shape is the cube
        edge = 20
        newCurve = cmds.curve(n = controlName, d = 1, p=[(-edge, edge, edge),
        (edge, edge, edge),
        (edge,-edge,edge),
        (-edge,-edge,edge),
        (-edge,edge,edge),
        (-edge,edge,-edge),
        (-edge,-edge,-edge),
        (-edge, -edge, edge),
        (-edge, edge, edge),
        (edge,edge,edge),
        (edge,edge,-edge),
        (-edge, edge, -edge),
        (-edge, -edge, -edge),
        (edge, -edge, -edge),
        (edge, edge, -edge),
        (edge,edge,edge),
        (edge, -edge, edge) ,
        (edge, -edge, -edge)], k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
    cmds.editDisplayLayerMembers('Controls', newCurve)
    cmds.move(jntTrans[0],jntTrans[1],jntTrans[2])
    cmds.makeIdentity(apply = True, t= 1, r= 1, s= 1, n= 0)
    cmds.connectAttr('%s.r' % newCurve, '%s.r' % jointName)
    if not amIRoot:
        cmds.parent(controlName, 'Control_%s' % parentJointName)
        #adding to a display layer is recursive by default, so only do on root
        cmds.editDisplayLayerMembers('Joints', cmds.ls(sl = True)[0])
#------------------------main()----------------------
@emailNotifyer
def createSkeletonControls():
    #setting up layers to put the joints and controls into
    cmds.createDisplayLayer(n ='Controls')
    cmds.createDisplayLayer(n ='Joints')

    #starting to find all the joints
    originalSelection = cmds.ls(sl = True)[0]
    allJoints = []
    allJoints.append(originalSelection)
    relativeList = cmds.listRelatives(allJoints[0], ad = True)
    #Maya recurses, so it goes from the bottom and returns up
    relativeList.reverse()
    for relative in relativeList:
        allJoints.append(relative)
    for i in range(0, len(allJoints)):
        if i == 0:
        #at the root
            createMayaBox(allJoints[i], '', True)
            continue
        parentName = cmds.listRelatives(allJoints[i], ap = True)[0]
        createMayaBox(allJoints[i], parentName, False)
    return cmds.select(originalSelection)
