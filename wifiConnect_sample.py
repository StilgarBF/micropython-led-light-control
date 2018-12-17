import network, time


def connect_wlan():
    nic = network.WLAN(network.STA_IF)
    ssid = 'myssid'
    wlan_pass = 'mypass'

    if nic.isconnected():
        print('Already connected. IP:')
        print(nic.ifconfig()[0])
        return

    nic.active(True)
    nic.connect(ssid, wlan_pass)

    while not nic.isconnected():
        print('waiting for connection .....')

        if not nic.isconnected():
            time.sleep(2)

    print('connection successful IP:')
    print(nic.ifconfig()[0])
