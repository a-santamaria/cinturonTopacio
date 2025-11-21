## Accelerometer and Gyroscope (WS2812B)

Pico 2           BMI160
|-------------------------|
3V3 (OUT)   -->  VIN
GND         -->  GND
GPI20 (SDA) -->  SDA
GPI21 (SCL) -->  SCL
3V3         -->  CS     (puts BMI160 into I2C mode)
GND         -->  SAO    (I2C address = 0x68)


## Led (WS2812B)

#### USB Power Banck

Pico 2           WS2812B                                
|-------------------------|
VSYS (5V IN)    -->  VCC (using usb power bacnk)
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

- Verde -> Datos