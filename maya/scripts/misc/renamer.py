import maya.cmds as cmds
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def appendRecurse(locationOfAppend, text, node):
    print 'Recursing on node: %s' % node
    children = cmds.listRelatives(node, c = True, ni = True)
    print children
    #syntax for popular !.IsEmpty() in python lists
    if children:
        print children
        for child in children:
            print child
            appendRecurse(locationOfAppend, text, child)
            
    if locationOfAppend == 'front':
        node = cmds.rename(node, text + node)
    else:
    #appending to the end
        node = cmds.rename(node, node + text)
        
@emailNotifyer
def appendName(locationOfAppend = 'end', Type = 'transform'):
    if Type == 'transform':
	#For handling appendning to Transforms/Joint names
        if locationOfAppend == 'end':
			#Button for appending to the end
            result = cmds.promptDialog( title='Append Transform/Joint Name: End', 
                                    message='Going to append currently selected transform, as well as all children, with inputted text.\nEX:\n   Inputted text = _SY\n   Selected transform name = root\n   Result for new name: root_SY   as well as all children nodes', 
                                    button=['Rename Selected', 'Rename All Children', 'Cancel'], 
                                    defaultButton='Rename Selected', 
                                    cancelButton='Cancel', 
                                    dismissString='Cancel')
            if result == 'Rename All Children':
                for node in cmds.ls(sl = True):
                    appendRecurse(locationOfAppend, cmds.promptDialog(query = True, text = True), node)
            elif result == 'Rename Selected':
                selectedNodes = cmds.ls(sl = True, sn = True)
                for node in selectedNodes:
                    node = cmds.rename(node, node + cmds.promptDialog(q = True, t = True))
            
            
        elif locationOfAppend == 'front':
			#Button for appending to the front
            result = cmds.promptDialog( title='Append Transform/Joint Name: Front', 
								message='Going to append currently selected transform, as well as all children, with inputted text.\nEX:\n   Inputted text = SY_\n   Selected transform name = root\n   Result for new name: SY_root   as well as all children nodes', 
                                button=['Rename Selected', 'Rename All Children', 'Cancel'], 
                                defaultButton='Rename Selected', 
                                cancelButton='Cancel', 
                                dismissString='Cancel')
            if result == 'Rename All Children':
                #User wants all children renamed as well
                for node in cmds.ls(sl = True):
                    appendRecurse(locationOfAppend, cmds.promptDialog(query = True, text = True), node)
            elif result == 'Rename Selected':
                selectedNodes = cmds.ls(sl = True, sn = True)
                for node in selectedNodes:
                    node = cmds.rename(node, cmds.promptDialog(q = True, t = True) + node)
					
	
    elif Type == 'mesh':
        #For handling appendning to mesh Names
        if locationOfAppend == 'front':		
            result = cmds.promptDialog( title='Append Mesh Name: Front', 
								message='Going to append all selected meshes with inputted text.\nEX:\n   Inputted text = SM_\n   Selected mesh name = Cat_House\n   Result for new name: SM_Cat_House', 
								button=['Rename','Rename all meshes', 'Cancel'], 
								defaultButton='Rename', 
								cancelButton='Cancel', 
								dismissString='Cancel')
            text = cmds.promptDialog(q = True, text = True)
            if result == 'Rename':
				#Use didn't cancel
				#Getting all the selected meshes in the scene
                allMeshes = cmds.ls(sl = True)
				#Itterating and setting new names
                for mesh in allMeshes:
                    newName = cmds.promptDialog(query = True, text = True) + mesh
                    mesh = cmds.rename(mesh, newName)
            elif result == 'Rename all meshes':
                result = cmds.confirmDialog(title = 'Appending to all meshes',
                                            message = 'About to edit all meshes in the scene, are you sure?',
                                            button = ['Yes', 'Cancel'],
                                            defaultButton = 'Yes',
                                            cancelButton = 'Cancel')
                if result == 'Yes':
                    #user really wants to rename those meshes
                    #Getting all the  meshes in the scene
                    allMeshes = cmds.ls(type = Type)
                    allMeshTransforms = []
                    for mesh in allMeshes:
                        allMeshTransforms.append(cmds.listRelatives(mesh, parent = True))
                    #Itterating and setting new names
                    for transform in allMeshTransforms:
                        newName = text + transform[0]
                        transform = cmds.rename(transform, newName)
                    
        elif locationOfAppend == 'end':
            result = cmds.promptDialog( title='Append Mesh Name: End', 
								message='Going to append all selected meshes with inputted text.\nEX:\n   Inputted text = _SM\n   Selected mesh name = Cat_House\n   Result for new name: Cat_House_SM', 
								button=['Rename', 'Rename all meshes', 'Cancel'], 
								defaultButton='Rename', 
								cancelButton='Cancel', 
								dismissString='Cancel')
								
            if result == 'Rename':
				#Getting all the meshes in the scene
				allMeshes = cmds.ls(sl = True)
				#Itterating and setting new names
				for mesh in allMeshes:
					newName = mesh + cmds.promptDialog(query = True, text = True)
					mesh = cmds.rename(mesh, newName)
            elif result == 'Rename all meshes':
                result = cmds.confirmDialog(title = 'Appending to all meshes',
                                            message = 'About to edit all meshes in the scene, are you sure?',
                                            button = ['Yes', 'Cancel'],
                                            defaultButton = 'Yes',
                                            cancelButton = 'Cancel')
                if result == 'Yes':
                    #user really wants to rename those meshes
                    #Getting all the  meshes in the scene
                    allMeshes = cmds.ls(type = Type)
                    allMeshTransforms = []
                    for mesh in allMeshes:
                        allMeshTransforms.append(cmds.listRelatives(mesh, parent = True))
                    #Itterating and setting new names
                    for transform in allMeshTransforms:
                        newName = transform[0] + cmds.promptDialog(query = True, text = True)
                        transform = cmds.rename(transform, newName)