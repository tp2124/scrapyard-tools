__doc__="""
Place to test tools failing to edit the email updater tool.
Just a file to practice the abstraction of the decorater
"""

from lib_error_emailUpdate import emailNotifyer

@emailNotifyer
def doSomethingStupid():
    dic = {}
    print dic['something']

doSomethingStupid()