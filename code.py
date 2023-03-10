# SPDX-FileCopyrightText: 2021 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT
try:
    import time
    import board
    import busio
    import adafruit_gps
    import notecard
    import json
    import supervisor
    from adafruit_neokey.neokey1x4 import NeoKey1x4

    # PROD
    # supervisor.disable_autoreload()
    # supervisor.runtime.auto_reload = False

    # initialize
    print("Widow's Might 1.0 by bradspry@gmail.com")

    # use STEMMA I2C bus
    i2c_bus = busio.I2C(board.SCL, board.SDA)

    # Create a NeoKey object
    neokey = NeoKey1x4(i2c_bus, addr=0x30)

    # Adafruit Mini GPS PA1010D
    gps = adafruit_gps.GPS_GtopI2C(i2c_bus)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")

    # Twilio
    twilio_from = "+17042221234"
    twilio_to = "+17043331234"

    # Blues Notehub.io
    productUID = "com.yourname.name:widows_might"

    # Blues Notecard Init
    card = notecard.OpenI2C(i2c_bus, 0, 0, debug=True)
    req = {"req": "hub.set"}
    req["product"] = productUID
    req["mode"] = "periodic"
    rsp = card.Transaction(req)

    # LTE Network Time
    # should be useful for dimming leds at night
    reqb = {"req": "card.time"}
    rspb = card.Transaction(reqb)
    rspb = str(rspb)
    rspb = rspb.replace("'", '"')
    ntp = json.loads(rspb)
    ntp = str(ntp["time"])
    # print("The LTE network time is: " + ntp)

    # ENV.DEFAULT REGISTERS LOCAL ENVIRONMENT VARIABLES ON NOTECARD FOR INITIAL TESTING
    # THESE WILL BE OVERRIDDEN ONCE YOU SET THEM USING NOTEHUB.IO

    # SET ELDER NAME
    req = {"req": "env.default"}
    req["name"] = "elder-name"
    req["text"] = "Mx. Elder Name"
    card.Transaction(req)

    # SET ELDER ADDRESS
    req = {"req": "env.default"}
    req["name"] = "elder-address"
    req["text"] = "123 Main Street, City, ST 12345"
    card.Transaction(req)

    # SET ELDER PHONE
    req = {"req": "env.default"}
    req["name"] = "elder-phone"
    req["text"] = "704-111-1234"
    card.Transaction(req)

    # SET ELDER'S CAREGIVER PHONE
    req = {"req": "env.default"}
    req["name"] = "caregiver-phone"
    req["text"] = "704-555-1234"
    card.Transaction(req)

    # GET ELDER NAME VAR
    req = {"req": "env.get"}
    req["name"] = "elder-name"
    rspp = card.Transaction(req)
    rspp = str(rspp)
    rspp = rspp.replace("'", '"')
    person_name = json.loads(rspp)
    person_name = str(person_name["text"])
    # print("ELDER NAME: " + person_name)

    # GET ELDER ADDRESS VAR
    req = {"req": "env.get"}
    req["name"] = "elder-address"
    rspa = card.Transaction(req)
    rspa = str(rspa)
    rspa = rspa.replace("'", '"')
    person_address = json.loads(rspa)
    person_address = str(person_address["text"])
    # print("ELDER ADDRESS: " + person_address)

    # GET ELDER PHONE VAR
    req = {"req": "env.get"}
    req["name"] = "elder-phone"
    rsph = card.Transaction(req)
    rsph = str(rsph)
    rsph = rsph.replace("'", '"')
    person_phone = json.loads(rsph)
    person_phone = str(person_phone["text"])
    # print("ELDER PHONE: " + person_phone)

    # GET ELDER'S CAREGIVER PHONE VAR
    req = {"req": "env.get"}
    req["name"] = "caregiver-phone"
    rsphc = card.Transaction(req)
    rsphc = str(rsphc)
    rsphc = rsphc.replace("'", '"')
    person_caregiver_phone = json.loads(rsphc)
    person_caregiver_phone = str(person_caregiver_phone["text"])
    # print("CAREGIVER PHONE: " + person_caregiver_phone)

    # states for key presses
    key_0_state = False
    key_1_state = False
    key_2_state = False
    key_3_state = False

    key_0_rgb = 0x4B0082
    key_1_rgb = 0xFFFF00
    key_2_rgb = 0xFF4500
    key_3_rgb = 0xA52A2A

    neokey.pixels[0] = key_0_rgb
    neokey.pixels[1] = key_1_rgb
    neokey.pixels[2] = key_2_rgb
    neokey.pixels[3] = key_3_rgb

    while True:
        gps.update()
        if gps.fix_quality != 1:
            # Try again if we don't have a fix
            print("Waiting for fix...")
            # uncomment the following four lines to enable red lit keys when there's no gps signal
            # neokey.pixels[0] = 0xFF0000
            # neokey.pixels[1] = 0xFF0000
            # neokey.pixels[2] = 0xFF0000
            # neokey.pixels[3] = 0xFF0000
            supervisor.reload()
            continue

        eye1 = gps.latitude
        eye2 = gps.longitude
        xeyes = "%s,%s" % (gps.latitude, gps.longitude)

        #  switch debouncing
        #  also turns off NeoPixel on release
        if not neokey[0] and key_0_state:
            key_0_state = False
            neokey.pixels[0] = 0x0
        if not neokey[1] and key_1_state:
            key_1_state = False
            neokey.pixels[1] = 0x0
        if not neokey[2] and key_2_state:
            key_2_state = False
            neokey.pixels[2] = 0x0
        if not neokey[3] and key_3_state:
            key_3_state = False
            neokey.pixels[3] = 0x0

        #  if 1st neokey is pressed...
        if neokey[0] and not key_0_state:
            key_0_state = True
            print("Button A: PRAYER VISIT Button")
            neokey.pixels[0] = 0x0
            neokey.pixels[1] = 0x0
            neokey.pixels[2] = 0x0
            neokey.pixels[3] = 0x0
            neokey.pixels[0] = key_0_rgb
            neokey.pixels[0] = 0x0
            time.sleep(0.25)
            neokey.pixels[0] = key_0_rgb
            time.sleep(0.25)
            neokey.pixels[0] = 0x0
            time.sleep(0.25)
            neokey.pixels[0] = key_0_rgb
            time.sleep(0.25)
            neokey.pixels[0] = 0x0
            time.sleep(0.25)
            neokey.pixels[0] = key_0_rgb
            time.sleep(0.25)
            neokey.pixels[0] = 0x0
            time.sleep(0.25)
            neokey.pixels[0] = key_0_rgb
            time.sleep(0.25)
            neokey.pixels[0] = 0x0
            time.sleep(0.25)
            neokey.pixels[0] = key_0_rgb
            time.sleep(0.25)
            neokey.pixels[0] = 0x0
            time.sleep(0.25)
            req = {"req": "note.add"}
            req["file"] = "sensors.qo"
            req["sync"] = True
            req["body"] = {"button0": "pressed", "xgps": xeyes}
            rsp = card.Transaction(req)
            reqt = {"req": "note.add"}
            reqt["file"] = "twilio.qo"
            reqt["sync"] = True
            reqt["body"] = {
                "body": "{} pressed PRAYER button!%0D%0A%0D%0AADDRESS:%0D%0A{}%0D%0A%0D%0AELDER#:%0D%0A{}%0D%0A%0D%0ACAREGIVER#:%0D%0A{}%0D%0A%0D%0A".format(
                    person_name, person_address, person_phone, person_caregiver_phone
                )
                + "MAP: https://www.google.com/maps/place/"
                + str(xeyes)
                + "",
                "from": twilio_from,
                "to": twilio_to,
            }
            rsp = card.Transaction(reqt)
            # green button on successful blues lte transmission
            neokey.pixels[0] = 0x00FF00
            time.sleep(5)
            supervisor.reload()

        #  if 2nd neokey is pressed...
        if neokey[1] and not key_1_state:
            key_1_state = True
            print("Button B: HANDY VISIT button")
            neokey.pixels[0] = 0x0
            neokey.pixels[1] = 0x0
            neokey.pixels[2] = 0x0
            neokey.pixels[3] = 0x0
            neokey.pixels[1] = key_1_rgb
            neokey.pixels[1] = 0x0
            time.sleep(0.25)
            neokey.pixels[1] = key_1_rgb
            time.sleep(0.25)
            neokey.pixels[1] = 0x0
            time.sleep(0.25)
            neokey.pixels[1] = key_1_rgb
            time.sleep(0.25)
            neokey.pixels[1] = 0x0
            time.sleep(0.25)
            neokey.pixels[1] = key_1_rgb
            time.sleep(0.25)
            neokey.pixels[1] = 0x0
            time.sleep(0.25)
            neokey.pixels[1] = key_1_rgb
            time.sleep(0.25)
            neokey.pixels[1] = 0x0
            time.sleep(0.25)
            neokey.pixels[1] = key_1_rgb
            time.sleep(0.25)
            neokey.pixels[1] = 0x0
            time.sleep(0.25)
            req = {"req": "note.add"}
            req["file"] = "sensors.qo"
            req["sync"] = True
            req["body"] = {"button1": "pressed", "xgps": xeyes}
            rsp = card.Transaction(req)
            reqt = {"req": "note.add"}
            reqt["file"] = "twilio.qo"
            reqt["sync"] = True
            reqt["body"] = {
                "body": "{} pressed HANDY button!%0D%0A%0D%0AADDRESS:%0D%0A{}%0D%0A%0D%0AELDER#:%0D%0A{}%0D%0A%0D%0ACAREGIVER#:%0D%0A{}%0D%0A%0D%0A".format(
                    person_name, person_address, person_phone, person_caregiver_phone
                )
                + "MAP: https://www.google.com/maps/place/"
                + str(xeyes)
                + "",
                "from": twilio_from,
                "to": twilio_to,
            }
            rsp = card.Transaction(reqt)
            neokey.pixels[1] = 0x00FF00
            time.sleep(5)
            supervisor.reload()

        #  if 3rd neokey is pressed...
        if neokey[2] and not key_2_state:
            key_2_state = True
            print("Button C: LAWN VISIT button")
            neokey.pixels[0] = 0x0
            neokey.pixels[1] = 0x0
            neokey.pixels[2] = 0x0
            neokey.pixels[3] = 0x0
            neokey.pixels[2] = key_2_rgb
            neokey.pixels[2] = 0x0
            time.sleep(0.25)
            neokey.pixels[2] = key_2_rgb
            time.sleep(0.25)
            neokey.pixels[2] = 0x0
            time.sleep(0.25)
            neokey.pixels[2] = key_2_rgb
            time.sleep(0.25)
            neokey.pixels[2] = 0x0
            time.sleep(0.25)
            neokey.pixels[2] = key_2_rgb
            time.sleep(0.25)
            neokey.pixels[2] = 0x0
            time.sleep(0.25)
            neokey.pixels[2] = key_2_rgb
            time.sleep(0.25)
            neokey.pixels[2] = 0x0
            time.sleep(0.25)
            req = {"req": "note.add"}
            req["file"] = "sensors.qo"
            req["sync"] = True
            req["body"] = {"button2": "pressed", "xgps": xeyes}
            rsp = card.Transaction(req)
            reqt = {"req": "note.add"}
            reqt["file"] = "twilio.qo"
            reqt["sync"] = True
            reqt["body"] = {
                "body": "{} pressed LAWN button!%0D%0A%0D%0AADDRESS:%0D%0A{}%0D%0A%0D%0AELDER#:%0D%0A{}%0D%0A%0D%0ACAREGIVER#:%0D%0A{}%0D%0A%0D%0A".format(
                    person_name, person_address, person_phone, person_caregiver_phone
                )
                + "MAP: https://www.google.com/maps/place/"
                + str(xeyes)
                + "",
                "from": twilio_from,
                "to": twilio_to,
            }
            rsp = card.Transaction(reqt)
            neokey.pixels[2] = 0x00FF00
            time.sleep(5)
            supervisor.reload()

        #  if 4th neokey is pressed...
        if neokey[3] and not key_3_state:
            key_3_state = True
            print("Button D: FOOD VISIT button")
            neokey.pixels[0] = 0x0
            neokey.pixels[1] = 0x0
            neokey.pixels[2] = 0x0
            neokey.pixels[3] = 0x0
            neokey.pixels[3] = key_3_rgb
            neokey.pixels[3] = 0x0
            time.sleep(0.25)
            neokey.pixels[3] = key_3_rgb
            time.sleep(0.25)
            neokey.pixels[3] = 0x0
            time.sleep(0.25)
            neokey.pixels[3] = key_3_rgb
            time.sleep(0.25)
            neokey.pixels[3] = 0x0
            time.sleep(0.25)
            neokey.pixels[3] = key_3_rgb
            time.sleep(0.25)
            neokey.pixels[3] = 0x0
            time.sleep(0.25)
            neokey.pixels[3] = key_3_rgb
            time.sleep(0.25)
            neokey.pixels[3] = 0x0
            time.sleep(0.25)
            req = {"req": "note.add"}
            req["file"] = "sensors.qo"
            req["sync"] = True
            req["body"] = {"button3": "pressed", "xgps": xeyes}
            rsp = card.Transaction(req)
            reqt = {"req": "note.add"}
            reqt["file"] = "twilio.qo"
            reqt["sync"] = True
            reqt["body"] = {
                "body": "{} pressed FOOD button!%0D%0A%0D%0AADDRESS:%0D%0A{}%0D%0A%0D%0AELDER#:%0D%0A{}%0D%0A%0D%0ACAREGIVER#:%0D%0A{}%0D%0A%0D%0A".format(
                    person_name, person_address, person_phone, person_caregiver_phone
                )
                + "MAP: https://www.google.com/maps/place/"
                + str(xeyes)
                + "",
                "from": twilio_from,
                "to": twilio_to,
            }
            rsp = card.Transaction(reqt)
            neokey.pixels[3] = 0x00FF00
            time.sleep(5)
            supervisor.reload()
except:
    supervisor.reload()
