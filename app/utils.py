import pyotp
from django.core.mail import send_mail

def send_otp(email):
    secret=pyotp.random_base32()
    totp=pyotp.TOTP(secret)
    otp=totp.now()
    send_mail("OTP",f"Your OTP: {otp}","admin@gmail.com",[email])
    return secret