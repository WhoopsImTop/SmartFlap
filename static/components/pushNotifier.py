from pushnotifier import PushNotifier as pn

pn = pn.PushNotifier('Elias4711', 'Anton17032000', 'katzenklappe', 'V2VBBV466C3V8E7DV2VBV2VB63CVDE7DFFBFKFTFFB')


def pushNotify():
    pn.send_image('/home/pi/Desktop/SmartFlap/static/pictures/picture-named.jpg', silent=False, devices=['vgWm'])