from threading import Thread
from django.core.mail import EmailMessage  

class EmailSendThread(Thread):
    def __init__(self, email_obj: EmailMessage):
        super().__init__()
        self.email_obj = email_obj  

    def run(self) -> None:
        try:
            self.email_obj.send()
        except Exception as e:
            print(f"Failed to send email: {e}")