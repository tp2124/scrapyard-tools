__author__ = 'primm'
__doc__ = '''
This is the HitBox generation and editing tool. This controls the data as well as the UI, at the bottom. 
'''

import maya.cmds as cmds
import os.path
import json
import os, stat
import re
import glob
import ConfigParser
from functools import partial
from lib_error_emailUpdate import emailNotifyer
CHARACTERNAMES = ['Feline',
                'Bear',
                'Kangaroo',
                'Phreak']


#---------------------------------------Helper Classes---------------------------------------#
#Container of all of the data for this frame. This will represent each frame of animation for each move.
#This will be made when the users move the 
class AnimationFrame(object):
    def __init__(self,frame):
        print "Creating a new Animation Frame"
        self.m_frameNumber = frame
        self.m_hitBoxes = []
        self.m_attackBoxes = []
    def clear(self):
        for index in xrange(len(self.m_hitBoxes) - 1, -1, -1):
            try:
                self.m_hitBoxes[index].clear()
                del self.m_hitBoxes[index]
            except:
                pass
        for index in xrange(len(self.m_attackBoxes) - 1, -1, -1):
            try:
                self.m_attackBoxes[index].clear()
                del self.m_attackBoxes[index]
            except:
                pass
        
    def toJson(self, useRootOffsetData=False): 
        #create basic structure, this will be eventually put into a 'frames' array in the overall structure
        data = { 'framenumber':self.m_frameNumber, 'attackboxes':[],'hitboxes':[] }

        #populate the hitboxes and attackboxes
        for index in range(len(self.m_hitBoxes)):
            if self.m_hitBoxes[index] is not None:
                data['hitboxes'].append(self.m_hitBoxes[index].toJson(useRootOffsetData))
        for index in range(len(self.m_attackBoxes)):
            if self.m_attackBoxes[index] is not None:
                data['attackboxes'].append(self.m_attackBoxes[index].toJson(useRootOffsetData))

        data_string = json.dumps(data,sort_keys=True)
        return data

    #sets the internal data according the the json, also creates the cubes below it and adds them (from json aswell)
    #right now it doesn't 'clear' the data before it sets it in, so we should probably do that
    def fromJson(self,data, useRootOffsetData=False, useZ=True, useY=True):
        self.m_frameNumber = data['framenumber']
        #loop through data's hitboxes, create the box and update its data from json
        for index in range(len(data['hitboxes'])):
            tempBox = CollisionBox("HitBox_%d_%d" % (self.m_frameNumber , index), index)
            tempBox.fromJson(data['hitboxes'][index], useRootOffsetData, useZ, useY)
            self.m_hitBoxes.append(tempBox)

        #Do the same for attackboxes
        for index in range(len(data['attackboxes'])):
            tempBox = CollisionBox("AttackBox_%d_%d" % (self.m_frameNumber , index), index)
            tempBox.fromJson(data['attackboxes'][index], useRootOffsetData, useZ, useY)
            self.m_attackBoxes.append(tempBox)

#Representation of the box data. It can be Attack, to hit other players, or Hit, boxes to be vulerable to attacks.
class CollisionBox(object):
    def __init__(self, name, index):
        self.m_name = name
        self.m_index = index
        #Do not allow designers to move vertices. They need to adjust the transformation and not the pivot.
        tempCube = cmds.polyCube(n = name, w = 100, h = 100, d = 0)[0]
        cmds.rotate(0, 90, 0, r=True, os=True)
        self.m_cube = tempCube
        self.m_layout = []
        self.m_effectNumber = -1
        if 'Attack' in self.m_name:
            self.b_isAttack = True
            self.m_effectNumber = 0
        else:
            self.b_isAttack = False
        #red or blue based off of type of box
        lambert = cmds.shadingNode('lambert', asShader=True) 
        cmds.select(self.m_cube)
        if "Attack" in self.m_name:
            cmds.setAttr ( (lambert + '.color'), 1.0, 0.0, 0.0, type = 'double3' )
        else :
            cmds.setAttr ( (lambert + '.color'), 0.0, 0.0, 1.0, type = 'double3' )
            
        cmds.setAttr ( (lambert + '.transparency'), 0.90,0.90,0.90, type= 'double3' )
        
        cmds.hyperShade( assign=lambert )
        
    def clearUI(self):
        try:
            cmds.deleteUI(self.m_layout)
        except:
            pass
        self.m_layout=[]
        
    def addUI(self):
        self.m_layout = collisionBoxGui(self)
        
    def clear(self):
        self.clearUI()
        cmds.delete(self.m_cube)
        
    #simply prints the jsonobject of this cube/hitbox - we should really rename this btw lol... cube? naw
    def toJson(self, useRootOffsetData=False):
        #create structure for the box, will be held in an array of hitboxes/attackboxes
        #for position we may need to subtract from root node or something, but for now it's relative to 0,0,0 so that should be chill
        self.updateData(useRootOffsetData)
        data = { 'width':round(self.m_width,2), 'height':round(self.m_height,2), 
                'offset':{ 'z':round(self.m_position[2],2), 'y':round(self.m_position[1],2) } }
        if self.m_effectNumber > -1:
            data['powerIndex'] = self.m_effectNumber
        data_string = json.dumps(data,sort_keys=True)
        return data
    def fromJson(self, data, useRootOffsetData=False, useZ=True, useY=True):
        self.m_width = data['width']
        self.m_height = data['height']
        self.m_effectNumber = data.get('powerIndex', -1)
        
        if useRootOffsetData:                
            #Add in offset
            rootPos = cmds.xform('Root', q=True, t=True)
            if useZ and useY:
                self.m_position = (0, data['offset']['y'] + rootPos[1], data['offset']['z'] + rootPos[2])
            elif useZ and not useY:
                self.m_position = (0, data['offset']['y'], data['offset']['z'] + rootPos[2])
            elif not useZ and useY:
                self.m_position = (0, data['offset']['y'] + rootPos[1], data['offset']['z'])
            else:
                #dealing with depricated data, before individual axis option was valid.
                #apply on both axis
                self.m_position = (0, data['offset']['y'] + rootPos[1], data['offset']['z'] + rootPos[2])
                
                
        else:
            self.m_position = (0, data['offset']['y'], data['offset']['z'])
        self.m_scale = (self.m_width/cmds.polyCube( self.m_name, q=True, w=True ),self.m_height/cmds.polyCube( self.m_name, q=True, h=True ), 0)
        cmds.xform( self.m_name, s = self.m_scale )
        cmds.xform( self.m_name, t = self.m_position )
        cmds.setAttr((self.m_name + '.visibility'), 0) #start off invisible when loading
        
    #resize dimensions of cube based off scale and position and stuff 
    def updateData(self, useRootOffsetData=False):
        if useRootOffsetData:
            #Take out offset
            useZ = cmds.checkBox(g_rootOffsetZBox, q=True, value=True)
            useY = cmds.checkBox(g_rootOffsetYBox, q=True, value=True)
            
            rootPosition = cmds.xform('Root', q=True, t=True)
            boxPosition = cmds.xform( self.m_name, q=True, t=True)
            
            #zero X because we don't care
            boxPosition[0] = 0
            if useZ and useY:
                #Both Axis offset
                boxPosition[1] = boxPosition[1] - rootPosition[1]
                boxPosition[2] = boxPosition[2] - rootPosition[2]
            elif useZ and not useY:
                boxPosition[2] = boxPosition[2] - rootPosition[2]
            elif not useZ and useY:
                boxPosition[1] = boxPosition[1] - boxPosition[1]
                
            self.m_position = boxPosition
            self.m_position = (round(self.m_position[0]),round(self.m_position[1]),round(self.m_position[2]))
            self.m_scale = cmds.xform( self.m_name, q=True, s=True, relative=True )
            self.m_width = round(cmds.polyCube( self.m_name, q=True, w=True ) * abs(self.m_scale[0]),2)
            self.m_height = round(cmds.polyCube( self.m_name, q=True, h=True ) * abs(self.m_scale[1]),2)
        else:
            self.m_position = cmds.xform( self.m_name, q=True, t=True ) #Finds the translation, we should probably be finding the point of hte bottom left corner?? 
            self.m_position = (round(self.m_position[0]),round(self.m_position[1]),round(self.m_position[2]))
            self.m_scale = cmds.xform( self.m_name, q=True, s=True, relative=True )
            self.m_width = round(cmds.polyCube( self.m_name, q=True, w=True ) * abs(self.m_scale[0]),2)
            self.m_height = round(cmds.polyCube( self.m_name, q=True, h=True ) * abs(self.m_scale[1]),2)
        

#---------------------------------------End Helper Classes---------------------------------------#

#---------------------------------------Global Variables and Functions---------------------------------------#

def getCharacterType():
    working_scene = cmds.file(exn=True, q=True)
    directories = working_scene.split('/')
    characterType = directories[-3]
    if characterType in CHARACTERNAMES:
        return characterType
    else:
        cmds.confirmDialog(title='Not Scrapyard Anim Opened', message='Have the animation scene open before starting this tool.\nOpen an animation file, and then launch again.')
        exit('This is OK')
        
g_animationFrames = []
g_animationName = 'unnamed'
g_currentFrame = 1
g_characterType = getCharacterType()

#On export update the manifest to make sure the game will know any new data exists. 
def updateManifest(jsonName):
    manifestPath = os.environ['SY_ROOT'] + '\\Jsons\\manifest.json'

    jsonData = {'manifest': [], 'otherinfo':'other stuff'}
    listOfHitboxJsons = []

    for root, dirs, files in os.walk(os.environ['SY_ROOT'] + '\\Jsons\\HitBoxes'):
        for file in files:
            if file.endswith('.json'):
                listOfHitboxJsons.append('HitBoxes\\' + file.split('.')[0])
    jsonData['manifest'] = listOfHitboxJsons

    #Getting file stats to make any existing file off of read-only from perforce.
    fileAtt = os.stat(manifestPath)[0]
    if (not fileAtt & stat.S_IWRITE):
        # File is read-only, so make it writeable
        os.chmod(manifestPath, stat.S_IWRITE)
    
    json_file=open(manifestPath, 'w')
    json_file.write(json.dumps(jsonData,sort_keys=True))
    json_file.close()
    
#Update data for the game to read
def exportJsons(self):
    g_jsonPath = os.environ['JSON_DIR']
    g_iniPath = os.environ['INI_DIR']
    g_jsons = []
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(g_iniPath, 'DefaultGame.ini'))
    #loop through json files and convert
    for name in glob.glob( os.path.join(g_jsonPath, '*.json') ):
        FILE = open(name,"r")
        data_string = FILE.read()
        FILE.close()
        data = json.loads(data_string)
        actualName = data['name']
        data_string = re.sub(r'\s', '', data_string)
        data_string = re.sub("\"", "\\\"", data_string)
        data_string = "\"" + data_string + "\"";
        config.set('MechGame.MechGame','+' + re.sub("node",'',actualName.lower()), data_string)
    config.write( open(os.path.join(g_iniPath, 'DefaultGame.ini'), 'wb') )
        

def loadJson(name):
    if name:
        path = os.environ['SY_ROOT']
        name = g_characterType + '_' + name
            
        name = path + "\\Jsons\\HitBoxes\\" + name + ".json"
        FILE = open(name,"r")
        data_string = FILE.read()
        data = json.loads(data_string)
        FILE.close()
        return data
    else:
        cmds.confirmDialog(title = 'No Animation Name', message = 'Please enter an animation name before loading.\nBe sure to have the right type selected')
  
def addGUIDataToJsonData(data):
    #Defaults for nonAttacks
    data['isAttack'] = '0'
    data['isGround'] = '1'
    data['AttackWeapon'] = ''
    data['AttackDirection'] = ''
    data['useRootOffset'] = '0'
    data['useZOffset'] = '1'
    data['useYOffset'] = '1'
    
    if cmds.checkBox(g_isAttackAnimation, q=True, value=True):
        data['isAttack'] = '1'
        
        if not cmds.checkBox(g_isGroundAttackCheckBox, q=True, value=True):
            data['isGround'] = '0'
            
        if cmds.checkBox(g_isMeleeAttackCheckBox, q=True, value=True):
            data['AttackWeapon'] = 'Melee'
        else:
            data['AttackWeapon'] = cmds.textScrollList(g_specialWeaponType, q=True, si=True)[0]
        
        data['AttackDirection'] = cmds.textScrollList(g_attackDirection, q=True, si=True)[0]
    
    if cmds.checkBox(g_rootOffsetBox, q=True, value=True):
        data['useRootOffset'] = '1'
        
    if not cmds.checkBox(g_rootOffsetZBox, q=True, value=True):
        data['useZOffset'] = '0'
        
    if not cmds.checkBox(g_rootOffsetYBox, q=True, value=True):
        data['useYOffset'] = '0'
    
    return data

#Dump out this animation's data
def saveJson(absFilePath,data):
    if absFilePath[1] != ':':
        path = os.environ['SY_ROOT']
        absFilePath = g_characterType + '_' + absFilePath
        absFilePath = path + "\\Jsons\\HitBoxes\\" + absFilePath + ".json"
    data = addGUIDataToJsonData(data)
    if os.path.exists(absFilePath):
        fileAtt = os.stat(absFilePath)[0]
        if(not fileAtt & stat.S_IWRITE):
            os.chmod(absFilePath, stat.S_IWRITE)

    FILE = open(absFilePath,"w")
    FILE.write(json.dumps(data,sort_keys=True, indent=4))
    FILE.close()
    #creating a user fedback window
    cmds.confirmDialog(title = 'Good Save', message = 'Saved data %s' % absFilePath)
    return absFilePath
    
def validateFrame():
    global g_currentFrame
    frame = int(cmds.currentTime(query=True)) #left some deprecated code here to move to first frame instead of previous
    if g_currentFrame != frame:
        cmds.currentTime( g_currentFrame, edit = True, update= True)
        cmds.select( clear=True )
        print "USER ERROR: Don't use the timeslider for now"
        return -1
    return frame

def toJson(useRootOffsetData):
    global g_currentFrame
    actualCurrentFrame = g_currentFrame
    
    g_animationName = cmds.textField(g_animationNameField,q=True,tx=True)
    data = {'name':g_animationName, 'frames':[] }
    for index in range(len(g_animationFrames)-1):
        g_currentFrame = index + 1
        cmds.currentTime( index + 1, edit = True, update= True)
        data['frames'].append(g_animationFrames[index+1].toJson(useRootOffsetData))
    data_string = json.dumps(data,sort_keys=True)
    
    cmds.currentTime(actualCurrentFrame, edit=True, update=True)
    g_currentFrame = actualCurrentFrame
    return data

def resetData():
    global g_currentFrame
    for index in xrange(len(g_animationFrames) - 1, -1, -1):
        try:
            g_animationFrames[index].clear()
            del g_animationFrames[index]
        except: 
            pass
    blankFrame = AnimationFrame(0) #placeholder
    g_animationFrames.append(blankFrame) #placeholder
    cmds.currentTime( 1, edit = True, update= True)
    cmds.textField(g_currentFrameField,e=True,ip=1,tx=1)
    g_currentFrame = 1
    
#loads the animation from a json
def fromJson(data):
    g_animationName = data['name']
    resetData()
    useRootOffsetData = False
    useZ = False
    useY = False
    
    if data['isAttack'] == '1':
        cmds.checkBox(g_isAttackAnimation, e=True, value=True)
        toggleIsAttack(True)
    else:
        cmds.checkBox(g_isAttackAnimation, e=True, value=False)
        toggleIsAttack(False)
    
    if data['isGround'] == '1':
        cmds.checkBox(g_isGroundAttackCheckBox, e=True, value=True)
        toggleIsGround(True)
    else:
        cmds.checkBox(g_isGroundAttackCheckBox, e=True, value=False)
        toggleIsGround(False)
    
    if 'AttackWeapon' in data.keys():
        if data['AttackWeapon'] == 'Melee':
            #Set Melee Checkbox
            cmds.checkBox(g_isMeleeAttackCheckBox, e=True, value=True)
            toggleSpecialAttack(True)
        else:
            cmds.checkBox(g_isMeleeAttackCheckBox, e=True, value=False)
            toggleSpecialAttack(False)
            
            cmds.textScrollList(g_specialWeaponType, e=True, si=data['AttackWeapon'])
            if data['isAttack'] == '1':
                setAnimationNameToAttackFormat()
    else:
        cmds.checkBox(g_isMeleeAttackCheckBox, e=True, value=False)
        toggleSpecialAttack(False)
    
    if 'AttackDirection' in data.keys():
        cmds.textScrollList(g_attackDirection, e=True, si=data['AttackDirection'])
        if data['isAttack'] == '1':
            setAnimationNameToAttackFormat()
        
    if 'useRootOffset' in data.keys():
        if data['useRootOffset'] == '1':
            useRootOffsetData = True
            cmds.checkBox(g_rootOffsetBox, e=True, value=True)
            toggleUseRootOffset(True)
        else:
            cmds.checkBox(g_rootOffsetBox, e=True, value=False)
            toggleUseRootOffset(False)
        
        if 'useZOffset' in data.keys():
            if data['useZOffset'] == '0':
                cmds.checkBox(g_rootOffsetZBox, e=True, value=False)
            else:
                cmds.checkBox(g_rootOffsetZBox, e=True, value=True)
                useZ = True
        
        if 'useYOffset' in data.keys():
            if data['useYOffset'] == '0':
                cmds.checkBox(g_rootOffsetYBox, e=True, value=False)
            else:
                cmds.checkBox(g_rootOffsetYBox, e=True, value=True)
                useY = True
    
    global g_currentFrame
    actualCurrentFrame = g_currentFrame
    
    for index in range(len(data['frames'])):
        if useRootOffsetData:
            #Moving the timeslider every frame to be able to get the root
            #xform for each frame to displace the boxes
            g_currentFrame = index + 1
            cmds.currentTime( index + 1, edit = True, update= True)
        
        tempFrame = AnimationFrame(index)
        tempFrame.fromJson(data['frames'][index], useRootOffsetData, useZ, useY)
        g_animationFrames.append(tempFrame)
        #Setting frame numbers of the animation to how much data was brought in. 
        if index == 0:
            cmds.textField(g_startingAnimationFrameNumber, e = True, text = data['frames'][index]['framenumber'])
        if index == len(data['frames']) - 1:
            cmds.textField(g_endingAnimationFrameNumber, e = True, text = data['frames'][index]['framenumber'])
    cmds.currentTime(actualCurrentFrame, edit=True, update=True)
    g_currentFrame = actualCurrentFrame
    
    showNewBoxesInView(1)
    
def addHitBox(self,fromButton=True):
    frame = validateFrame()
   
    if frame == -1:
        return
    tempBox = CollisionBox("HitBox_%d_%d" % (frame , len(g_animationFrames[frame].m_hitBoxes)), len(g_animationFrames[frame].m_hitBoxes)) 
    if fromButton==True:
        tempBox.addUI()
    g_animationFrames[frame].m_hitBoxes.append(tempBox)

    return tempBox

def removeHitBox(self):
    frame = validateFrame()
    if frame == -1:
        return
    
def addAttackBox(self,fromButton=True):
    frame = validateFrame()
    if frame == -1:
        return
    tempBox = CollisionBox("AttackBox_%d_%d" % (frame , len(g_animationFrames[frame].m_attackBoxes)), len(g_animationFrames[frame].m_attackBoxes))
    if fromButton==True:
        tempBox.addUI()
    g_animationFrames[frame].m_attackBoxes.append(tempBox)
    return tempBox

def removeAttackBox(self):
    validateFrame()

#@emailNotifyer
def saveAnim(self):

    jsonFilePath = saveJson(cmds.textField(g_animationNameField,q=True,tx=True),
                            toJson(cmds.checkBox(g_rootOffsetBox, q=True, value=True)))
    updateManifest(jsonFilePath)

#@emailNotifyer
def loadAnim(self):
    fromJson(loadJson(cmds.textField(g_animationNameField,q=True,tx=True)))
    cmds.select(cl=True)
    
def LastFrame(self):
    currentFrame = validateFrame()
    if currentFrame == -1:
        return
    if currentFrame >= 1:
        if isFrameRangeSet():
            if currentFrame > int(cmds.textField(g_startingAnimationFrameNumber,q=True,tx=True)):
                changeToLastFrame(currentFrame)
            else:
                cmds.confirmDialog(m = "Trying to get outside of the set animation range.\nCurrentFrame: %d | Starting: %d | Ending: %d" % \
                    (currentFrame, int(cmds.textField(g_startingAnimationFrameNumber,q=True,tx=True)), int(cmds.textField(g_endingAnimationFrameNumber,q=True,tx=True))))
        else:
            changeToLastFrame(currentFrame)
            print "USER WARNING: should consider setting the animation range."
    else:
        print "USER ERROR: Trying to go to time 0 and below."
    cmds.select( clear=True )

def changeToLastFrame(currentFrame):
    removeBoxesFromView(currentFrame)
    cmds.currentTime( currentFrame - 1, edit = True, update= True)
    showNewBoxesInView(frame = int(cmds.currentTime( query=True )))
    cmds.textField(g_currentFrameField,e=True,ip=1,tx=currentFrame-1)
    global g_currentFrame
    g_currentFrame = currentFrame-1

    
def NextFrame(self): 
    currentFrame = validateFrame()
    if currentFrame == -1:
        return
    if isFrameRangeSet():
        if currentFrame < int(cmds.textField(g_endingAnimationFrameNumber,q=True,tx=True)):
            changeToNextFrame(currentFrame)
            showNewBoxesInView(frame = int(cmds.currentTime( query=True )))
            cmds.select( clear=True )
        else: 
            cmds.confirmDialog(m = "Trying to get outside of the set animation range.\nCurrentFrame: %d | Starting: %d | Ending: %d" % \
                (currentFrame, int(cmds.textField(g_startingAnimationFrameNumber,q=True,tx=True)), int(cmds.textField(g_endingAnimationFrameNumber,q=True,tx=True))))
    else:
        changeToNextFrame(currentFrame)
        showNewBoxesInView(frame = int(cmds.currentTime( query=True )))
        print "USER WARNING: should consider setting the animation range."
        
def changeToNextFrame(currentFrame):
    removeBoxesFromView(currentFrame)
    cmds.currentTime( currentFrame + 1, edit = True, update= True)
    cmds.textField(g_currentFrameField,e=True,ip=1,tx=currentFrame+1)
    global g_currentFrame
    g_currentFrame = currentFrame+1
    if len(g_animationFrames)==currentFrame+1: #makes a new frame, lets make some new hitboxes too brada
        blankFrame = AnimationFrame(currentFrame+1)
        g_animationFrames.append(blankFrame)
        for index in range(len(g_animationFrames[currentFrame].m_hitBoxes)):
            if g_animationFrames[currentFrame].m_hitBoxes[index] != None:
                tempBox = addHitBox(None,False)
                tempBox.fromJson(g_animationFrames[currentFrame].m_hitBoxes[index].toJson(cmds.checkBox(g_rootOffsetBox, q=True, value=True)))
        for index in range(len(g_animationFrames[currentFrame].m_attackBoxes)):
            if g_animationFrames[currentFrame].m_attackBoxes[index] != None:
                tempBox = addAttackBox(None,False)
                tempBox.fromJson(g_animationFrames[currentFrame].m_attackBoxes[index].toJson(cmds.checkBox(g_rootOffsetBox, q=True, value=True)))
	
	
    
def isFrameRangeSet():
    if cmds.textField(g_startingAnimationFrameNumber,q=True,tx=True).isdigit() and cmds.textField(g_endingAnimationFrameNumber,q=True,tx=True).isdigit():
        return True
    else:
        return False
    
#Handles updating all representations of the data
def removeBoxesFromView(currentFrame):
    for index in range(len(g_animationFrames[currentFrame].m_hitBoxes)):
        if g_animationFrames[currentFrame].m_hitBoxes[index] != None:
            cmds.setAttr((g_animationFrames[currentFrame].m_hitBoxes[index].m_name + '.visibility'), 0)
            g_animationFrames[currentFrame].m_hitBoxes[index].clearUI()
    for index in range(len(g_animationFrames[currentFrame].m_attackBoxes)):
        if g_animationFrames[currentFrame].m_attackBoxes[index] != None:
            cmds.setAttr((g_animationFrames[currentFrame].m_attackBoxes[index].m_name + '.visibility'), 0)
            g_animationFrames[currentFrame].m_attackBoxes[index].clearUI()

#Handles updating all representations of the data
def showNewBoxesInView(frame):
    for index in range(len(g_animationFrames[frame].m_hitBoxes)):
        if g_animationFrames[frame].m_hitBoxes[index] != None:
            cmds.setAttr((g_animationFrames[frame].m_hitBoxes[index].m_name + '.visibility'), 1)
            g_animationFrames[frame].m_hitBoxes[index].addUI()
    for index in range(len(g_animationFrames[frame].m_attackBoxes)):
        if g_animationFrames[frame].m_attackBoxes[index] != None:
            cmds.setAttr((g_animationFrames[frame].m_attackBoxes[index].m_name + '.visibility'), 1)
            g_animationFrames[frame].m_attackBoxes[index].addUI()
 
def DeleteLastFrame(self):
    #Delete second to last frame, keep the ghost frame leading.
    goodIndex = len(g_animationFrames) - 1
    res = cmds.confirmDialog( title='Delete Frame', message='About to delete frame: %d' % goodIndex, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

    if res == 'No':
        return
    #Removing the model data
    g_animationFrames.remove(g_animationFrames[goodIndex])
    newNumberOfFrames = len(g_animationFrames) - 1

    #Deleting the transform of the boxes
    allObjects = cmds.ls()
    lastFramesBoxes = []

    for obj in allObjects:
        if '_%d_' % (goodIndex) in obj and cmds.objectType(obj) == 'transform':
            lastFramesBoxes.append(obj)
    for box in lastFramesBoxes:
        cmds.delete(box)

    #Changing end number of the Animation GUI
    cmds.textField(g_endingAnimationFrameNumber, e = True, text = newNumberOfFrames)
	
def setTimeSlider(self):
    pass
	# print "Trying to set Time Slider"
	
#---------------------------------------End Global Variables and Functions---------------------------------------#




def collisionBoxGui(box):
    boxName = box.m_name
    boxIndex = box.m_index
    box.updateData()
    
    def toggleVisibility(self):
        if cmds.getAttr(( boxName + '.visibility'))==1:
            cmds.setAttr(( boxName + '.visibility'), 0)
        else:
            cmds.setAttr(( boxName + '.visibility'), 1)
    def toggleSelect(self):
        #cmds.setAttr(( boxName + '.visibility'), 1)
        cmds.select(boxName,tgl=True) #,visible=True 
    def selectOnly(self):
        cmds.select(clear=True)
        cmds.select(boxName)
    def deleteGUIBox(self, layout):
        currentFrame = validateFrame()
        cmds.setParent( layout )
        if 'HitBox' in boxName:
            g_animationFrames[currentFrame].m_hitBoxes[boxIndex].clearUI()
            g_animationFrames[currentFrame].m_hitBoxes[boxIndex] = None
            cmds.delete("HitBox_%d_%d" % ( currentFrame, boxIndex))
        else:
            g_animationFrames[currentFrame].m_attackBoxes[boxIndex].clearUI()
            g_animationFrames[currentFrame].m_attackBoxes[boxIndex] = None
            cmds.delete("AttackBox_%d_%d" % ( currentFrame, boxIndex))
    def cycleEffectNumber(self):
        box.m_effectNumber += 1
        if box.m_effectNumber > 5:
            box.m_effectNumber = 0
        cmds.textField(guiEffectNumber, e=True, tx=box.m_effectNumber)
    
    if 'HitBox' in boxName:
        boxColor = [0.2, 0.3, 1.0]
    else:
        boxColor = [0.5, 0.0, 0.0]
    cmds.setParent(g_frameHolder)
    cmds.setParent(g_column)

    m_layout = cmds.frameLayout( label=boxName, borderStyle='in',w = 450, backgroundColor = boxColor , 
                                collapsable = True, collapse=False)
    cmds.rowColumnLayout(numberOfColumns=6)
    
    cmds.button(l = "Toggle Selection", c = partial(toggleSelect))
    cmds.button(l = "Select Only This", c = partial(selectOnly))
    cmds.button(l = "Toggle Visibility", c = partial(toggleVisibility))
    cmds.button(l = "Delete Box", c = partial(deleteGUIBox, layout = m_layout))
    #Lazy spacers
    cmds.text(l='')
    cmds.text(l='')
    
    cmds.text( label='Width' )
    cmds.textField(cmds.textField(editable=False),e=True,tx=box.m_width)
    
    cmds.text( label='Offset z' )
    cmds.textField(cmds.textField(editable=False),e=True,tx=box.m_position[2])

    if box.b_isAttack:
        cmds.text( label='Effect #')
        guiEffectNumber = cmds.textField(cmds.textField(editable=True), e=True,tx=box.m_effectNumber)
    else:
        cmds.text(l='')
        cmds.text(l='')
            
    cmds.text( label='Height' )
    cmds.textField(cmds.textField(editable=False),e=True,tx=box.m_height)
    
    cmds.text( label='Offset y' )
    cmds.textField(cmds.textField(editable=False),e=True,tx=box.m_position[1])

    if box.b_isAttack:
        cmds.button(l = 'Cycle Effect #', c=partial(cycleEffectNumber))

    
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    return m_layout


def setAnimationNameToAttackFormat():
    if cmds.checkBox(g_isAttackAnimation, q=True, value=True):
        generatedName = ''
        if cmds.checkBox(g_isGroundAttackCheckBox, q=True, value=True):
            generatedName += 'Ground_'
        else:
            generatedName += 'Air_'
        
        if cmds.checkBox(g_isMeleeAttackCheckBox, q=True, value=True):
            generatedName += 'Melee_'
        else:
            #is a special weapon anim
            selectedSpecial = cmds.textScrollList(g_specialWeaponType, q=True, si=True)[0]
            if selectedSpecial == 'Elemental Gauntlets':
                generatedName += 'Elemental_'
            elif selectedSpecial == 'Flux Rifle':
                generatedName += 'Flux_'
            elif selectedSpecial == 'Traps':
                generatedName += 'Traps_'
        
        selectedDirection = cmds.textScrollList(g_attackDirection, q=True, si=True)[0]
        if selectedDirection == 'Forward':
            generatedName += 'Forward'
        elif selectedDirection == 'Backward':
            generatedName += 'Backward'
        elif selectedDirection == 'Lunge':
            generatedName += 'Lunge'
        elif selectedDirection == 'Up':
            generatedName += 'Up'
        elif selectedDirection == 'Down':
            generatedName += 'Down'
        elif selectedDirection == 'Neutral':
            generatedName += 'Neutral'
        cmds.textField(g_animationNameField, e=True, tx=generatedName)
    
#Attack GUI visibilty toggling
"""
TODO: update g_attackDirection's append to represent only the proper direction
based on if it is a in air/ground special/melee attack
"""
def toggleIsAttack(checkBoxValue):
    global g_attackOnlyGUI
    if checkBoxValue:
        cmds.rowColumnLayout(g_attackOnlyGUI, e=True, visible=True)
        cmds.textField(g_animationNameField, e=True, editable=False)
        setAnimationNameToAttackFormat()
    else:
        cmds.rowColumnLayout(g_attackOnlyGUI, e=True, visible=False)
        cmds.textField(g_animationNameField, e=True, editable=True)
        setAnimationNameToAttackFormat()
    
def toggleSpecialAttack(checkBoxValue):
    global g_specialAttackOnlyGUI
    if checkBoxValue:
        cmds.rowColumnLayout(g_specialAttackOnlyGUI, e=True, visible=False)
        setAnimationNameToAttackFormat()
    else:
        cmds.rowColumnLayout(g_specialAttackOnlyGUI, e=True, visible=True)
        setAnimationNameToAttackFormat()

def toggleIsGround(checkBoxValue):
    if cmds.checkBox(g_isAttackAnimation, q=True, value=True):
        setAnimationNameToAttackFormat()
    
def toggleUseRootOffset(checkBoxValue):
    if checkBoxValue:   
        cmds.rowColumnLayout(g_rootOffsetAxisLayout, e=True, visible=True)
    else:
        cmds.rowColumnLayout(g_rootOffsetAxisLayout, e=True, visible=False)
        
def offsetAxisChanged(checkBoxValue):
    if not cmds.checkBox(g_rootOffsetZBox, q=True, value=True) and not cmds.checkBox(g_rootOffsetYBox, q=True, value=True):
        #Both boxes were changed to False
        cmds.confirmDialog(title='Offset Something', message='You should not have neither axis being exported while trying to use root based offsets')
        cmds.checkBox(g_rootOffsetZBox, e=True, value=True)
    
#---------------------------------------GUI Initialization---------------------------------------#
GUIwindow = cmds.window(t = "Scrapyard Hit Box Tool", s = 1, w = 450, h = 800)

scrlayout = cmds.scrollLayout( 'scrollLayout' )
cmds.frameLayout( label='General', borderStyle='in', collapsable=True )
generalLayout = cmds.rowColumnLayout(numberOfColumns=4, w = 450, 
                                    columnWidth = [(1,80), (2,145), (3,80), (4,145)])

cmds.text( label='Animation Name' )
g_animationNameField = cmds.textField()
g_isAttackAnimation = cmds.checkBox(label='Is Attack', value=False, changeCommand=toggleIsAttack)
cmds.setParent( '..' )

g_attackOnlyGUI = cmds.rowColumnLayout(vis=False, numberOfColumns=3, 
                                        columnWidth = [(1, 80), (2, 80), (3, 300)])
g_isGroundAttackCheckBox = cmds.checkBox(label='Is Ground', value=True, 
                                        changeCommand=toggleIsGround)
g_isMeleeAttackCheckBox = cmds.checkBox(label='Is Melee', value=True, changeCommand=toggleSpecialAttack)
g_specialAttackOnlyGUI = cmds.rowColumnLayout(vis=False, numberOfColumns=2, 
                                            columnWidth = [(1,100), (2,150)])
cmds.text(label='Special Type')
g_specialWeaponType = cmds.textScrollList(append=['Elemental Gauntlets', 'Flux Rifle', 'Traps'], 
                                    selectItem = 'Elemental Gauntlets', h = 32,
                                    selectCommand = setAnimationNameToAttackFormat)
cmds.setParent('..')
cmds.text(label='Direction')
g_attackDirection = cmds.textScrollList(append=['Forward', 'Up', 'Down', 'Neutral', 'Lunge', 'Backward'], 
                                    selectItem = 'Forward', h = 32,
                                    selectCommand = setAnimationNameToAttackFormat)
cmds.setParent('..')

cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,112), (2,300)])
g_rootOffsetBox = cmds.checkBox(label='Root Offset Data', value=False,
                                changeCommand=toggleUseRootOffset)
g_rootOffsetAxisLayout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,100), (2,100)],
                                                visible=False)
g_rootOffsetZBox = cmds.checkBox(label='Offset Z', value=True, changeCommand=offsetAxisChanged)
g_rootOffsetYBox = cmds.checkBox(label='Offset Y', value=True, changeCommand=offsetAxisChanged)

cmds.setParent('..')
cmds.setParent('..')
                                
cmds.rowColumnLayout(numberOfColumns=4, columnWidth = [(1, 112), (2, 112), (3,224)])
SaveAnimButton = cmds.button(l = "Save Anim", c = partial(saveAnim))
LoadAnimButton = cmds.button(l = "Load Anim",c = partial(loadAnim))
cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [(1,75), (2, 50), (3, 50)])
cmds.text( label = 'Range of Anim')
g_startingAnimationFrameNumber = cmds.textField(text = "Start" )
g_endingAnimationFrameNumber = cmds.textField(text = "End")
cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.frameLayout( label = 'Controls', borderStyle='in')
heightOfNewButtons = 50
cmds.rowColumnLayout(numberOfColumns=2, height = heightOfNewButtons, columnWidth=[(1,225),(2,225)])
AddAttBoxButton = cmds.button(l = "New Attackbox", h = heightOfNewButtons-4, c = partial(addAttackBox))
AddHitBoxButton = cmds.button(l = "New Hitbox", h = heightOfNewButtons-4, c = partial(addHitBox))


cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.frameLayout( label='Frame Control', borderStyle='in' )
cmds.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,225),(2,225)])

cmds.text( label='Current Frame' )
g_currentFrameField = cmds.textField(editable=False)
cmds.textField(g_currentFrameField,e=True,it=1)

cmds.rowColumnLayout(numberOfColumns=2)
DeleteLastFrameButton = cmds.button(l = "Delete Last Frame", c = partial(DeleteLastFrame))

cmds.setParent( '..' )
cmds.rowColumnLayout(numberOfColumns=2)
MovePastFrameButton = cmds.button(l = "<<", c = partial(LastFrame))
MoveNextFrameButton = cmds.button(l = ">>", c = partial(NextFrame))

cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
g_frameHolder = cmds.frameLayout( label='Current Frame', borderStyle='out' )
g_column = cmds.columnLayout(columnWidth=450)

cmds.setParent( '..' )
cmds.setParent( '..' )



cmds.showWindow( GUIwindow ) 
#---------------------------------------End GUI Initialization---------------------------------------#
if len(g_animationFrames)==0:
    blankFrame = AnimationFrame(0) #placeholder
    g_animationFrames.append(blankFrame) #placeholder
    blankFrame1 = AnimationFrame(1) #first frame
    g_animationFrames.append(blankFrame1) #first frame

