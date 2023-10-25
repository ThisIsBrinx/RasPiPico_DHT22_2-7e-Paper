# Bibliotheken laden
from machine import Pin, lightsleep, freq
from dht import DHT22
from epaper import EPD_2in7

# Initialisierung GPIO und DHT22
dht22_sensor = DHT22(Pin(2, Pin.IN, Pin.PULL_UP))

#adjust your timeout !!!
timeoutInMinutes = 1

epd = EPD_2in7()
epd.EPD_2IN7_Init()

marginLeftCol1 = 45
marginLeftCol2 = 170
marginLeftNumber = 5

marginTop = 5
lineSpace = 15

timeout = timeoutInMinutes * 1000 * 60
maxMessurement = 11

request = 1

temp = []
humi = []

#Taktfrequenz reduzieren
freq(100000000) 

# Wiederholung (Endlos-Schleife)
while True:
    i=1    

    # Messung durchführen
    dht22_sensor.measure()
    # Werte lesen
    newtemp = dht22_sensor.temperature()
    newhumi = dht22_sensor.humidity()
    
    epd.image1Gray_Landscape.fill(0xff)
    #epd.image1Gray_Portrait.fill(0xff)
    
    #heading
    epd.image1Gray_Landscape.text("Temperatur", marginLeftCol1, marginTop, epd.black)
    epd.image1Gray_Landscape.text("Luftfeuchte", marginLeftCol2, marginTop, epd.black)

    #current state
    epd.image1Gray_Landscape.text("last", marginLeftNumber, marginTop + lineSpace, epd.black)
    epd.image1Gray_Landscape.text(str(newtemp) + "C", marginLeftCol1, marginTop + (lineSpace), epd.black)
    epd.image1Gray_Landscape.text(str(newhumi) + "%", marginLeftCol2, marginTop + (lineSpace), epd.black)

    temp.append(newtemp)
    humi.append(newhumi)

    print("request: " + str(request))

    while i < request:
        print("in")
        j = request - i

        epd.image1Gray_Landscape.text("-" + str(i) + "m", marginLeftNumber, marginTop + (lineSpace + (lineSpace * i)), epd.black)
        epd.image1Gray_Landscape.text(str(temp[j-1]) + "C", marginLeftCol1, marginTop + (lineSpace + (lineSpace * i)), epd.black)
        epd.image1Gray_Landscape.text(str(humi[j-1]) + "%", marginLeftCol2, marginTop + (lineSpace + (lineSpace * i)), epd.black)
        
        i=i+1

    epd.EPD_2IN7_Display_Landscape(epd.buffer_1Gray_Landscape)
    #epd.EPD_2IN7_4Gray_Display(epd.buffer_4Gray)
    
    if request >= maxMessurement:
        print("true")
        temp.pop(0)
        humi.pop(0)
        request = request - 1
        
    request = request + 1

    lightsleep(timeout)