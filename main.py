# Bibliotheken laden
from machine import Pin, lightsleep, freq
from dht import DHT22
from epaper import EPD_2in7

# Initialisierung GPIO und DHT22
dht22_sensor = DHT22(Pin(2, Pin.IN, Pin.PULL_UP))

epd = EPD_2in7()
epd.EPD_2IN7_Init()

marginLeftCol1 = 45
marginLeftCol2 = 170
marginLeftNumber = 5

marginTop = 5
lineSpace = 15

timeoutInMinutes = 1
timeout= timeoutInMinutes * 100 * 1
maxMessurement = 48

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
    # Werte ausgeben    
    
    epd.image1Gray_Landscape.fill(0xff)
    #epd.image1Gray_Portrait.fill(0xff)
    #epd.image4Gray.fill(0xff)
      
    
    #heading
    epd.image1Gray_Landscape.text("Temperatur", marginLeftCol1, marginTop, epd.black)
    epd.image1Gray_Landscape.text("Luftfeuchte", marginLeftCol2, marginTop, epd.black)

    #current state
    epd.image1Gray_Landscape.text("last", marginLeftNumber, marginTop + lineSpace, epd.black)
    epd.image1Gray_Landscape.text(str(newtemp) + "C", marginLeftCol1, marginTop + (lineSpace), epd.black)
    epd.image1Gray_Landscape.text(str(newhumi) + "%", marginLeftCol2, marginTop + (lineSpace), epd.black)

    temp.append(newtemp)
    humi.append(newhumi)

    while i < request:
        j = request - i

        print("i: " + str(i))
        print("request: " + str(request))
        if i <= 6:
            print("lower then 6")
            epd.image1Gray_Landscape.text("-" + str(i) + "h", marginLeftNumber, marginTop + (lineSpace + (lineSpace * i)), epd.black)
            epd.image1Gray_Landscape.text(str(temp[j-1]) + "C", marginLeftCol1, marginTop + (lineSpace + (lineSpace * i)), epd.black)
            epd.image1Gray_Landscape.text(str(humi[j-1]) + "%", marginLeftCol2, marginTop + (lineSpace + (lineSpace * i)), epd.black)
            epd.EPD_2IN7_Display_Landscape(epd.buffer_1Gray_Landscape)
        elif i == 12:
            print("12")
            epd.image1Gray_Landscape.text("-" + str(i) + "h", marginLeftNumber, marginTop + (lineSpace + (lineSpace * 5)), epd.black)
            epd.image1Gray_Landscape.text(str(temp[j-1]) + "C", marginLeftCol1, marginTop + (lineSpace + (lineSpace * 5)), epd.black)
            epd.image1Gray_Landscape.text(str(humi[j-1]) + "%", marginLeftCol2, marginTop + (lineSpace + (lineSpace * 5)), epd.black)
            epd.EPD_2IN7_Display_Landscape(epd.buffer_1Gray_Landscape)
        elif i == 24:
            print("24")
            epd.image1Gray_Landscape.text("-" + str(i) + "h", marginLeftNumber, marginTop + (lineSpace + (lineSpace * 6)), epd.black)
            epd.image1Gray_Landscape.text(str(temp[j-1]) + "C", marginLeftCol1, marginTop + (lineSpace + (lineSpace * 5)), epd.black)
            epd.image1Gray_Landscape.text(str(humi[j-1]) + "%", marginLeftCol2, marginTop + (lineSpace + (lineSpace * 5)), epd.black)
            epd.EPD_2IN7_Display_Landscape(epd.buffer_1Gray_Landscape)


        i=i+1

    
    #epd.EPD_2IN7_4Gray_Display(epd.buffer_4Gray)
       
    if request >= maxMessurement:
        temp.pop(0)
        humi.pop(0)
        request = request - 1
        
    request = request + 1

    lightsleep(timeout)