import requests
from django.conf import settings


def send_sms(receiver_number, message):
    post_data = {
        'UserName': settings.SMS_USERNAME,
        'Password': settings.SMS_PASSWORD,
        'PhoneNumber': settings.SMS_PHONE_NUMBER,
        'MessageBody': message,
        'RecNumber': receiver_number,
        'Smsclass': '1',
    }
    response = requests.post('https://RayganSMS.com/SendMessageWithPost.ashx', post_data)
    return response
