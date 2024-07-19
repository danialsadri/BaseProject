import threading


def send_sms(phone_number, otp_code):
    return None


class SMSThread(threading.Thread):
    def __init__(self, phone_number, otp_code):
        self.phone_number = phone_number
        self.otp_code = otp_code

        threading.Thread.__init__(self)

    def run(self):
        send_sms(self.phone_number, self.otp_code)


def send_sms_thread(phone_number, otp_code):
    SMSThread(phone_number, otp_code).start()
