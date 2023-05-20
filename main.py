import time
import urequests as requests
import network
import machine
import mfrc522

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect('FabLab', 'FabLab66')
    while not sta_if.isconnected():
        pass
print(sta_if.ifconfig())

url_users = 'https://pastebin.com/raw/GU8CPJM7'
url_ntfy = 'https://ntfy.sh/FabLabGuest'

def myusers():
    users = []
    try:
        res = requests.get(url_users)
        for user in (res.text).split('\n'):
            user = user.replace('\r', '')
            user = user.split(':')[1]
            users.append(user)
    except:
        pass
    print(users)
    res = requests.post(url_ntfy, data=users)
    return 0

rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
def badge_lu():
    time.sleep(1)
    # Détecte la présence d'un badge
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    print(stat)
    if stat == rdr.OK:

        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            # Affichage du type de badge et de l'UID
            print("\nBadge détecté !")
            print(" - type : %03d" % tag_type)
            print(" - uid : %03d.%03d.%03d.%03d" %
                        (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))

            # Affichage des données en mémoire
            if rdr.select_tag(raw_uid) == rdr.OK:
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                    print(" - données : %s" % rdr.read(8))
                    rdr.stop_crypto1()
                # Affichage en cas de problème
                else:
                    print("Erreur de lecture")
            # Affichage en cas de problème
            else:
                print("Erreur badge")
    return "%s.%s.%s.%s" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
def main():
    myusers()
    while True:
        print("hello")
        uid = badge_lu()
        print(uid)
if __name__ == '__main__':
    main()
