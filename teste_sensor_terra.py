from machine import ADC, Pin
import time

# Sensores
umidade = ADC(26)  # GP26
luz = ADC(27)      # GP27

# Saída no pino 22
saida = Pin(22, Pin.OUT)

while True:
    valor_umidade = umidade.read_u16()
    valor_luz = luz.read_u16()
    saida.value(1)

    print("Umidade:", valor_umidade)
    print("Luz:", valor_luz)
    
    time.sleep(5)
    # Verifica valor da luz
    if valor_umidade > 60000:
        saida.value(0)  # Liga pino 22
        time.sleep(0.5)
        saida.value(1)
        print("Pino 22 ATIVADO")
    print("----------------------")

    time.sleep(1)