import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
user_reguex = "^[a-zA-Z0-9_.-]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


    
def isUsernameValid(user):
    if user=="usuario":
        return True
    else:
        return False
        
def isPasswordValid(password):
    if password=="usuario":
        return True
    else:
        return False

def isUsernameValidm(user):
    if user=="medico":
        return True
    else:
        return False
        
def isPasswordValidm(password):
    if password=="medico":
        return True
    else:
        return False

def isUsernameValidp(user):
    if user=="paciente":
        return True
    else:
        return False
        
def isPasswordValidp(password):
    if password=="paciente":
        return True
    else:
        return False

