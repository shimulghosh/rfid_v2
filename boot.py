import time
import urequests as requests
import network
from machine import Pin
from machine import SoftSPI
from mfrc522 import MFRC522

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect('Freebox-427DB4', 'dirigebam26-prosaicos&-edidisti-linxi3')
    while not sta_if.isconnected():
        pass
print(sta_if.ifconfig())
rdr = MFRC522(0, 2, 4, 5, 14)
print("Place card")
rfid_names = ["N1", "N2","B1"]
rfid_uids = ["0xc9d36c98ee", "009.012.146.152","0x597cd6986b"]

def get_username(uid):
    index = -1
    try:
        index = rfid_uids.index(uid)
        return rfid_names[index]
    except ValueError:
        print("RFID not recognized")
        return 0

temps=time.localtime()
jour_premierbadge=temps[2]
print(jour_premierbadge)
i=0
jour_nouveaubadge=jour_premierbadge
while jour_nouveaubadge==jour_premierbadge:
    temps_ecoule=time.localtime()
    jour=temps_ecoule[2]
    jour_nouveaubadge=jour
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            i=i+1
            print(i,"badges passes")
            card_id = "0x%02x%02x%02x%02x%02x" % tuple(raw_uid)
            print(card_id)

            # Si l'utilisateur existe, il est pris en compte
            username = get_username(card_id)
            if username != 0:
                print("Welcome {}".format(username))
            else:
                print("Access denied")

            # Si l'utilisateur n'existe pas, il est appelé "Quelqu'un"
