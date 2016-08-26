__doc__="""
Library to handle notifying when an exception happens.
"""

import smtplib
import sys
from collections import namedtuple
#from PyQt4 import QtGui, QtCore
#email: scrapyardtools@gmail.com. pword: scrapyard

"""
Carrier Email to SMS Gateway
*****************************************************************


Alltel                          [10-digit phone number]@message.alltel.com
                Example: 1234567890@message.alltel.com

AT&T (formerly Cingular)        [10-digit phone number]@txt.att.net
                                [10-digit phone number]@mms.att.net (MMS)
                                [10-digit phone number]@cingularme.com
                Example: 1234567890@txt.att.net

Boost Mobile                    [10-digit phone number]@myboostmobile.com
                Example: 1234567890@myboostmobile.com

Nextel (now Sprint Nextel)  [10-digit telephone number]@messaging.nextel.com
                Example: 1234567890@messaging.nextel.com

Sprint PCS (now Sprint Nextel)  [10-digit phone number]@messaging.sprintpcs.com
                                [10-digit phone number]@pm.sprint.com (MMS)
                Example: 1234567890@messaging.sprintpcs.com

T-Mobile                    [10-digit phone number]@tmomail.net
                Example: 1234567890@tmomail.net

US Cellular                 [10-digit phone number]email.uscc.net (SMS)
                                [10-digit phone number]@mms.uscc.net (MMS)
                Example: 1234567890@email.uscc.net

Verizon                         [10-digit phone number]@vtext.com
                                [10-digit phone number]@vzwpix.com (MMS)
                Example: 1234567890@vtext.com

Virgin Mobile USA           [10-digit phone number]@vmobl.com
                Example: 1234567890@vmobl.com

*****************************************************************
"""

#For provider, supports: AT&T, Verizon, T-Mobile, Sprint
#For phone number, format with no punctuation. EX: 2145324336
Contact = namedtuple('Contact', ['name', 'emailAddr', 'phoneNumber', 'phoneProvider'])

LIST_OF_RECIPIENTS = [Contact('Travis Primm', 'someOther@gmail.com', '1234567890', 'AT&T'),
                        ]

"""
class emailerNotifyWidget(QtGui.QWidget):
    def __init__(self, *args):
        super(emailerNotifyWidget, self).__init__()
        #General Window stuff
        self.move(300, 200)

        msg = 'A tool has failed, and an e-mail has been sent to:'
        for name in LIST_OF_RECIPIENTS:
            msg += '\n\t' + name
        msg += '\n' + 'Please check proper usage/call one of the recipients if it is time sensative.'

        self.assetLabel = QtGui.QLabel(msg)
        self.exitButton = QtGui.QPushButton('OK')
        self.connect(self.exitButton,
            QtCore.SIGNAL('clicked()'),
            self.exit)
"""

def emailError(message, sourceTraceback):
    #Connecting to the SY tools e-mail account
    server = smtplib.SMTP('smtp.gmail.com',587)	#creates a server object with the correct port if we are using gmail
    server.set_debuglevel(0)
    server.ehlo()		#handshaking for the esmtp server
    server.starttls()	#starts TLS services with Gmail, because gmail uses TLS (Transport Layer Security)
    server.login('scrapyardtools@gmail.com', 'scrapyard')

    #Putting the file doc in a try/except because we are nooblie programmers who don't write __doc__ for all files
    fileDoc = str(sourceTraceback.func_globals['__doc__'])
    scriptPath = '\\' + str(sourceTraceback.func_code.co_filename).split('Scrapyard')[-1]

    #Check to see if none
    #try:
    
    # Formatting message to include data about where the script was being run from
    message = 'Module that had the error:' + scriptPath + '.\n\nFunction that had Error: ' + sourceTraceback.func_name + \
                '(). On line: ' + str(sourceTraceback.func_code.co_firstlineno) +'\n\nFunction Doc:' + fileDoc + '\n\n+++Error Summary+++\n' + message
    
    for contact in LIST_OF_RECIPIENTS:
        text = 'From: [Scrapyard Tool Error] <scrapyardtools@gmail.com>\nTo:Tool Master <' +\
                contact.emailAddr + '>\nSubject: Problem with: %s\n\n' % scriptPath + message
        server.sendmail('scrapyardtools@gmail.com', contact.emailAddr, text)
        if contact.phoneProvider:
            #Send text
            textEmailAddr = contact.phoneNumber
            if contact.phoneProvider == 'AT&T':
                textEmailAddr += '@txt.att.net'
            elif contact.phoneProvider == 'Verizon':
                textEmailAddr += '@vtext.com'
            elif contact.phoneProvider == 'T-Mobile':
                textEmailAddr += '@tmomail.net'
            elif contact.phoneProvider == 'Sprint':
                textEmailAddr += '@messaging.sprintpcs.com'


            text = 'From: [Scrapyard Tool Error] <scrapyardtools@gmail.com>\nTo:Tool Master <' +\
                    textEmailAddr + '>\nSubject: Problem with: %s\n\n' % scriptPath + message
            server.sendmail('scrapyardtools@gmail.com', textEmailAddr, text)



def emailNotifyer(original_function):
    #This is a known as a decorator.
    # Consider of wrapping other code in this
    # And this catches and exceptions and emails back with error details
    # Active when you see @emailNotifer above other functions
    def wrapper(*args, **kwargs):
        try:
            original_function(*args, **kwargs)
        except:
            errorType, severity, traceback = sys.exc_info()
            originalError = traceback.tb_frame.f_locals['original_function']

            emailMsg = 'figure this out later, if there is anything useful to put here'
            emailError(emailMsg, originalError)

            feedbackMsg = '\nThis is embarassing...\nA tool has failed, and an e-mail has been sent to:'
            for contact in LIST_OF_RECIPIENTS:
                feedbackMsg += '\n\t' + contact.emailAddr + ', ' + contact.name
            feedbackMsg += '\n' + 'Please check proper usage or call one of the recipients if it is time sensative.'

            #window = emailerNotifyWidget()
        
    return wrapper
