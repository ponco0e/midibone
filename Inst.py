#By ponco
import sys
import Adafruit_BBIO.GPIO as GPIO


#TODO: Poner un offset de GPIO's para usar multiples instrumentos (maybe an static var?). DERP!
#TODO: Modificar noteOn() y noteOff() para multicanal
class Instrument:
    
    note2mid = {"As3":58 , "C4":60 , "D4":62 , "Ds4":63 , "F4":65 , "G4":67 , "A4":69 , "As4":70 , "C5":72}    #TODO: Write dict
    bbb_gpios = ["P9_11","P9_12","P9_13"]      #TODO: Put all the gpios that can be used safely as outputs (o los que se puedan)

    
    def __init__(self , note2buttons , actuatorno , isinv , chan): #initialize con lista de notas (en notacion anglosajona), numero de puchabotones necesarios, si se usa logica negada y el canal MIDI a escuchar
        self.actuatorno = actuatorno
        self.isinv = isinv
        self.chan=chan #Not implemented
        self.mid2gpio = self.__convert2Gpios(note2buttons) #obtener los gpios necesarios a encender o apagar cuando llega un msg de noteOn o noteOff
        for i in range(0 , actuatorno):
            GPIO.setup(self.bbb_gpios[i], GPIO.OUT)
        

    def __del__(self):
        GPIO.cleanup()
        print("DBG: Instrument: SelfDestruct")
    

    def __convert2Gpios(self , d): #devuelve un dict como el del argumento, solo que con una lista de gpios de bbb en vez de senales en binario
        retval = dict()
        for i in d: #por cada llave del dict d...
            if self.note2mid.has_key(i):
                retval[self.note2mid[i]] = self.__obtainGpioNames(d[i])    #...si la tabla de notas a hex la tiene, entonces anade al dict de retorno...
            else: 
                raise ValueError("La lista de notas a botones discretos esta mal formada") #...si no, la nota esta mal escrita
        print ("DBG: Instrument.__convert2Gpios(): " , retval)
        return retval
            
          
    def __obtainGpioNames(self , byteg): #convierte el byte que representa los botones a una lista de cadenas con los nombres de los gpios a prender
        retval = []
        if self.isinv:
            for i in range(0 , self.actuatorno): 
                if byteg % 2 is 0:
                    retval.append(self.bbb_gpios[i]) #por cada bit en el byte que representa los botones, si el LSB es 0 (negado) se agregara el i-esimo GPIO en notacion de texto
                byteg = byteg // 2
        else:
            for i in range(0 , self.actuatorno): 
                if byteg % 2 is 1:
                    retval.append(self.bbb_gpios[i]) #Si no es negado, tons se hace lo mismo pero buscando un LSB igual a 1
                byteg = byteg // 2
        return retval
    
    
    def noteOn(self , n): #turn on actuators
        if self.mid2gpio.has_key(n):
            if self.isinv:
                for e in self.mid2gpio[n]:
                    GPIO.output(e, GPIO.LOW)
            else:
                for e in self.mid2gpio[n]:
                    GPIO.output(e, GPIO.HIGH)
            print("DBG: Instrument.noteOn(): ",self.mid2gpio[n])
        else: print("DBG: Instrument.noteOn(): Ignore")
    
    
    def noteOff(self , n): #turn off actuators
        if self.mid2gpio.has_key(n):
            if self.isinv:
                for i in range(0,self.actuatorno):
                    GPIO.output(self.bbb_gpios[i], GPIO.HIGH)
            else: 
                for i in range(0,self.actuatorno):
                    GPIO.output(self.bbb_gpios[i], GPIO.LOW)
            print("DBG: Instrument.noteOff(): ",self.mid2gpio[n])
        else: print("DBG: Instrument.noteOff(): Ignore")