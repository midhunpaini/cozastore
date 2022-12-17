from twilio.rest import Client
from django.conf import settings


class MessageHandler:
    phone_no = None
    otp = None
    
    def __init__(self, phone_no, otp) -> None:
        self.phone_no = phone_no
        self.otp = otp
        
    def send_otp(self):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
                                body=self.otp,
                                from_='+12057546186',
                                to=self.phone_no
                                )
