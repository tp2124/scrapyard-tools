__author__ = 'primm'
__doc__ = '''
This is the exporter. This will handle making sure assets are exported with the proper fbx
settings to be able to be used in Unreal Engine 3.
'''

import maya.cmds as cmds
import os, stat
import maya.mel as mel
import shutil
from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def exportStaticMesh():
    #Load the plugin
    plugin = 'fbxmaya'

    if not cmds.pluginInfo(plugin, query = True, loaded = True):
        cmds.loadPlugin(plugin)

    preset = os.environ['SY_TOOLS_DIR'] + ('\\maya\\UDK_StaticMesh.fbxexportpreset')
    preset = preset.replace('\\', '\\\\')
    #load fbx preset
    cmd = 'FBXLoadExportPresetFile -f "%s";' % preset
    mel.eval(cmd)
    #export the selected mesh
    selected_object = cmds.ls(sl = True)[0]
    cmd = 'FBXExport -f %s.fbx -s;' % selected_object
    mel.eval(cmd)

    #Move the .fbx
    working_scene = cmds.file(exn=True, q=True)
    current_scene_dir = working_scene.split('/')
    current_scene_dir.pop()
    current_scene_dir.append(selected_object + '.fbx')
    fbx_file = '\\'.join(current_scene_dir)

    #were going to get the export dir from the working dir
    export_path = working_scene.split('/')
    for i in range(len(export_path)):
        if export_path[i] == 'Assets':
            export_path[i+1] = 'Export'
            export_path[i+4] = 'StaticMesh'
            if len(export_path) > i+5:
                for j in range(i+5,len(export_path)):
                    export_path.pop()
            break
        if i == len(export_path):
            #user isnt working in proper art directories
            pass

    #Formatting paths for files
    export_dir = '\\'.join(export_path)
    export_path.append(selected_object + '.fbx')
    export_file = '\\'.join(export_path)
    
    try:
        #Trying to make the directory if its a first SM
        os.makedirs(export_dir)
    except WindowsError:
        #Its cool, dir already exists
        pass

    #Getting file stats to make any existing file off of read-only from perforce.
    try:
        fileAtt = os.stat(export_file)[0]
        if (not fileAtt & stat.S_IWRITE):
            # File is read-only, so make it writeable
            os.chmod(export_file, stat.S_IWRITE)
    except:
        #this .fbx doesn't exist yet, don't try to change its privaleges.
        pass

    shutil.move(fbx_file,export_file)
    
@emailNotifyer
def exportAnimation():
    #Load the plugin
    plugin = 'fbxmaya'

    if not cmds.pluginInfo(plugin, query = True, loaded = True):
        cmds.loadPlugin(plugin)

    preset = os.environ['SY_TOOLS_DIR'] + ('\\maya\\UDK_Animation.fbxexportpreset')
    preset = preset.replace('\\', '\\\\')
    
    #load the preset
    cmd = 'FBXLoadExportPresetFile -f "%s";' % preset
    mel.eval(cmd)
    #export the fbx
    file_path = cmds.file(q = True, sn = True)
    file_path_list =  file_path.split('/')
    scene_name = file_path_list[len(file_path_list)-1]
    scene_name = scene_name.split('.')
    scene_name.pop()
    export_name = scene_name[0]
    cmd = 'FBXExport -f %s.fbx -s;' % export_name
    mel.eval(cmd)
    
    #Move the .fbx
    working_scene = cmds.file(exn=True, q=True)
    current_scene_dir = working_scene.split('/')
    current_scene_dir.pop()
    current_scene_dir.append(export_name + '.fbx')
    fbx_animation_file = '\\'.join(current_scene_dir)

    #were going to get the export dir from the working dir
    export_path = working_scene.split('/')
    for i in range(len(export_path)):
        if export_path[i] ==  'Assets':
            export_path[i+1] = 'Export'
            export_path[i+4] = 'Animations'
            if len(export_path) > i+5:
                for j in range(i+5,len(export_path)):
                    export_path.pop()
            break
        if i == len(export_path):
            #user isnt working in proper art directories
            pass
    #Formatting paths for files
    export_dir = '\\'.join(export_path)
    export_path.append(export_name + '.fbx')
    export_file = '\\'.join(export_path)
    
    try:
        #Trying to make the directory if its a first Anim
        os.makedirs(export_dir)
    except WindowsError:
        #Its cool, dir already exists
        pass

    #Getting file stats to make any existing file off of read-only from perforce.
    try:
        fileAtt = os.stat(export_file)[0]
        if (not fileAtt & stat.S_IWRITE):
            # File is read-only, so make it writeable
            os.chmod(export_file, stat.S_IWRITE)
    except:
        #this .fbx doesn't exist yet, don't try to change its privaleges.
        pass

    shutil.move(fbx_animation_file,export_file)
    

def exportSkeletalMesh():
    #Load the plugin
    plugin = 'fbxmaya'

    if not cmds.pluginInfo(plugin, query = True, loaded = True):
        cmds.loadPlugin(plugin)

    preset = os.environ['SY_TOOLS_DIR'] + ('\\maya\\UDK_SkeletalMesh.fbxexportpreset')
    preset = preset.replace('\\', '\\\\')
    #load fbx preset
    cmd = 'FBXLoadExportPresetFile -f "%s";' % preset
    mel.eval(cmd)
    #export the selected mesh
    count = 0
    
    for object in cmds.ls(sl = True):
        print object
        if cmds.objectType(object) == 'joint':
            count += 1
        elif cmds.objectType(object) == 'transform':
            count +=1
        else: 
           print "Selected something that is not a joint or gemoetry"
           return 
    
    if count < 2: 
        object = cmds.ls(sl = True)
        if object[0] != 'Root':    
            print "Root not selected"
            return
        else:
            print "No Geometry selected"
            return
            
    selected_object = cmds.ls(sl = True)
    for x in range(0,len(selected_object)):
        selected_object[0] = selected_object[0].replace("|","_")
  
    if count == 2:
        if selected_object[0] == 'Root':
            file_name = selected_object[1]
            cmd = 'FBXExport -f %s.fbx -s;' % file_name
        else:
            file_name = selected_object[0]
            cmd = 'FBXExport -f %s.fbx -s;' % file_name
   
    else:
        print "Wall"
        file_name = "multi_mesh_export"
        if selected_object[0] != 'Root':
            file_name = "%s_multi_mesh_export" % selected_object[0]
            cmd = 'FBXExport -f %s.fbx -s;' % file_name
        else:
             file_name = "%s_multi_mesh_export" % selected_object[1]
             cmd = 'FBXExport -f %s.fbx -s;' % file_name
    print cmd
    mel.eval(cmd)

    #Move the .fbx
    working_scene = cmds.file(exn=True, q=True)
    current_scene_dir = working_scene.split('/')
    current_scene_dir.pop()
    current_scene_dir.append(file_name + '.fbx')
    fbx_file = '\\'.join(current_scene_dir)

    #were going to get the export dir from the working dir
    export_path = working_scene.split('/')
    for i in range(len(export_path)):
        if export_path[i] == 'Assets':
            export_path[i+1] = 'Export'
            export_path[i+4] = 'SkeletalMesh'
            if len(export_path) > i+5:
                for j in range(i+5,len(export_path)):
                    export_path.pop()
            break
        if i == len(export_path):
            #user isnt working in proper art directories
            pass
    #Formatting paths for files
    export_dir = '\\'.join(export_path)
    export_path.append(file_name + '.fbx')
    export_file = '\\'.join(export_path)
    
    try:
        #Trying to make the directory if its a first Skeletal
        os.makedirs(export_dir)
    except WindowsError:
        #Its cool, dir already exists
        pass

    #Getting file stats to make any existing file off of read-only from perforce.
    try:
        fileAtt = os.stat(export_file)[0]
        if (not fileAtt & stat.S_IWRITE):
            # File is read-only, so make it writeable
            os.chmod(export_file, stat.S_IWRITE)
    except:
        #this .fbx doesn't exist yet, don't try to change its privaleges.
        pass
    print fbx_file
    print export_file
    shutil.move(fbx_file,export_file)
