import machine, time
import wifiConnect
import usocket as socket
import _thread

poti_1 = machine.ADC(machine.Pin(32))
poti_1.atten(poti_1.ATTN_11DB)
poti_2 = machine.ADC(machine.Pin(33))
poti_2.atten(poti_2.ATTN_11DB)

led_1 = machine.PWM(machine.Pin(25))
led_1.duty(0)
led_2 = machine.PWM(machine.Pin(26))
led_2.duty(0)

# establish connection
wifiConnect.connect_wlan()

html = """ foooo"""


def ana2pwm(analog_in):
    pwmVal = 1030 / 4096 * analog_in
    pwmVal = round(pwmVal / 10) * 10

    if pwmVal > 1023:
        pwmVal = 1023

    return round(pwmVal)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)


def web_process():
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)
    LEDON0 = request.find('/?LED=ON0')
    LEDOFF0 = request.find('/?LED=OFF0')
    LEDON2 = request.find('/?LED=ON2')
    LEDOFF2 = request.find('/?LED=OFF2')

    if LEDON0 == 6:
        print('TURN LED0 ON')
    if LEDOFF0 == 6:
        print('TURN LED0 OFF')
    if LEDON2 == 6:
        print('TURN LED2 ON')
    if LEDOFF2 == 6:
        print('TURN LED2 OFF')
    response = html
    conn.send(response)
    conn.close()


_thread.start_new_thread(web_process, ())

while True:
    potVal = poti_1.read()
    pwmValue = ana2pwm(potVal)
    led_1.duty(pwmValue)
    print('potiValue1: ' + '% 5d' % potVal + ' | pwmValue 1: ' + '% 5d' % pwmValue)

    potVal = poti_2.read()
    pwmValue = ana2pwm(potVal)
    led_2.duty(pwmValue)
    print('potiValue2: ' + '% 5d' % potVal + ' | pwmValue 2: ' + '% 5d' % pwmValue)
    print('#########')
    time.sleep_ms(200)

print('##### out ')
