# -*- coding: utf-8 -*-

# Defines function TextMeWhenDone.
# Sends a text message and email to the specified recipients once the given 
# time-consuming function has completed running or is interrupted by an error. 
# Useful when you want to be alerted that your simulations are finished or 
# your neural net is done training.

# First you must (very easily) set up an App password for your Gmail account:
# https://support.google.com/accounts/answer/185833?hl=en

# If you want to text a phone with a carrier other than those below, refer to
# the list below and add a new carrier_suffixes key:
# Some phone carrier SMS formats: http://www.makeuseof.com/tag/email-to-sms/ 
# (Has only been tested on AT&T phone)

import smtplib
import time



def TextMeWhenDone(phone_carrier,phone_10digits,gmail_address,gmail_APP_password,process,**process_args_dict):
    """
    phone_carrier: string
                   Carrier company. One of: 'AT&T', 'T-Mobile', 'Verizon', 'Virgin'
    
    phone_10digits: string of length 10
                   String of the 10 digit phone number to which to send text message
                   
    gmail_address: string
                   String of the gmail address to send FROM, including suffix "@gmail.com"
    
    gmail_APP_password: string of length 16
                   String of sender's gmail account App password
                   
    process: function
                   The function to execute, after which the phone number will be alerted.
                   
    **process_args_dict: dictionary
                   Dictionary of arguments for function "process". Format:
                   {'param1':value1,'param2':value2,...,'paramN':valueN}
    """
    
    # SMS suffixes for common carriers. If other carrier desired, refer to link
    carrier_suffixes = {'AT&T':'txt.att.net', 'T-Mobile':'tmomail.net', 'Verizon':'vtext.com', 'Virgin':'vmobl.com'}
    
    # Try executing the function with the given arguments, except all errors
    try:
        process(**process_args_dict)
        endtime = time.strftime("%H:%M:%S on %m/%d/%Y",time.localtime())
        body = 'Process completed successfully at '
        TEXT = body + endtime
        SUBJECT = 'SUCCESS'
    except Exception as error:
        endtime = time.strftime("%H:%M:%S on %m/%d/%Y",time.localtime())
        body = 'Process failed at '
        TEXT = body + endtime + '\n' + error.__class__.__name__ + ': ' + error.message
        SUBJECT = 'FAILURE'
    
    # Email parameters
    domain = carrier_suffixes[phone_carrier]
    FROM = gmail_address
    TO = [FROM,"{0}@{1}".format(phone_10digits,domain)] #Email and text yourself

    # Prepare message content
    content = """\From: {0}\nTo: {1}\nSubject: {2}\n\n{3}""".format(FROM,', '.join(TO),SUBJECT,TEXT)
    
    # Send message
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_address, gmail_APP_password)
    server.sendmail(FROM, TO, content)
    server.close()
    print 'Successfully sent the SMS'
    
    
    
    
if __name__ == '__main__':
    
    # Make up some function to simulate another function that takes a long time to run
    def VeryLongProcess(max_number,pause_time=1):
        i = 0
        while i <= max_number:
            time.sleep(pause_time)
            print i
            i+=1
        #intentionally_fail = undefined
            
    
    # Test function TextMeWhenDone:
    kwargs = {'max_number':10,'pause_time':1}
    TextMeWhenDone('AT&T','415-------','...@gmail.com','16letters',VeryLongProcess,**kwargs)