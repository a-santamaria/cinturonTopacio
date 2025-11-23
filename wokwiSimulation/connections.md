## Accelerometer and Gyroscope (WS2812B)

Pico 2           BMI160
|-------------------------|
3V3 (OUT)   -->  VIN
GND         -->  GND
GPI10 (SDA) -->  SDA
GPI11 (SCL) -->  SCL
3V3         -->  CS     (puts BMI160 into I2C mode)
GND         -->  SAO    (I2C address = 0x68)


## Led (WS2812B)

#### USB Power Banck

Pico 2           WS2812B                                
|-------------------------|
VBUS (5V USB)    -->  VCC (using usb power bank)
GPI22           -->  IN
GND             -->  GND
OUT             -->  Next Led

#### USB AA battery + V5 boost regulator (POLOLU-2564)

Battery      POLOLU-2564      WS2812B     Pico 2
|----------------------------------------------------|
RED       -->   VIN
BLACK     -->   GND     -->     GND  -->   GND
                VOUT    -->     VCC
                VOUT                 -->   VSYS
                                IN   <--   GPI22


## Codigo de clor

- Amarillo - Rojo - Naranja -> energia

- Negro - Gris - Azul -> ground

- Verde - Morado - Blanco -> Datos