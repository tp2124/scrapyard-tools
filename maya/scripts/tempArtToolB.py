import maya.cmds as cmds

def foo():
    result = cmds.confirmDialog( title='Confirm', 
                            message='Temp Art Tool B woot woot.', 
                            button=['Yes','No'], 
                            defaultButton='Yes', 
                            cancelButton='No', 
                            dismissString='No' )
    print result