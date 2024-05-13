 //Librerías que necesitamos
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include <SD.h>

#define SSpin 10  //Módulo microSD conectado ao pin 10

Adafruit_BMP280 bmp;  // Renomeamos o sensor bmp

int paquete = 0;// Variable para identificar o número de paquete enviado.
float TEMPERATURA, PRESION, PRESION_0, ALTITUDE, peltier, V_peltier;  //un float é un número con decimais (6 ou 7 decimais).

File logFile;  //Variable para o nome dos datos na SD.

void setup() {
  pinMode(A0, INPUT);  //Pin para a lectura da Voltaxe Peltier

  Serial.begin(9600);

  //Iniciamos o bmp280
  if (!bmp.begin(0x76)) {
    Serial.print("BMP280 no encontrado!");
    while (1)
      ;
  }

  PRESION_0 = bmp.readPressure() / 100.;  //Lemos a presión a nivel do chan, para calcular a altura respecto ao chan.

  //Iniciamos o módulo de la tarjeta SD
  Serial.println(F("Iniciando SD..."));
  if (!SD.begin(SSpin)) {
    Serial.println(F("Error al iniciar"));
    return;
  }
  Serial.println(F("Iniciado correctamente"));

  //Escribimos un primeiro texto na SD para identificar o bloque de datos de cada medida.
  logFile = SD.open("datos.txt", FILE_WRITE);
  if (logFile) {
    logFile.println("Comezamos!!");
    logFile.close();
  } else {
    Serial.println("Error al abrir el archivo en la tarjeta SD");
  }
}

void loop() {
  //Lemos os sensores
  TEMPERATURA = bmp.readTemperature();  //lectura da temperatura en grados centígrados
  PRESION = bmp.readPressure() / 100;   //lectrua da presión en hPa (por iso divido entre 100)
  ALTITUDE = bmp.readAltitude(PRESION_0); //lectura da altitude (necesita o dato a nivel do mar PRESION_0)
  peltier = analogRead(A0);             //lectura da Voltaxe peltier
  V_peltier = peltier / 1023 * 5.0;

  //Imprimimos identificador do Cansat (Muxia) e o número de paquete e enviámolas ao receptor do APC220
  Serial.print("Muxia, ");  //Con este identificador aseguramos que o dato é do noso CanSat
  Serial.print(paquete);
  Serial.print(",");

  //Imprimimos as variables no porto serie e no receptor.
  Serial.print(TEMPERATURA);
  Serial.print(",");
  Serial.print(PRESION);
  Serial.print(",");
  Serial.print(ALTITUDE);
  Serial.print(",");
  Serial.println(V_peltier, 3);

  //Gardamos os datos na SD
  logFile = SD.open("datos.txt", FILE_WRITE);
  if (logFile) {
    logFile.print(paquete);
    logFile.print(",");
    logFile.print(TEMPERATURA);
    logFile.print(",");
    logFile.print(PRESION);
    logFile.print(",");
    logFile.print(ALTITUDE);
    logFile.print(",");
    logFile.println(V_peltier, 3);
    logFile.close();
  } 
  else {
    Serial.println("Error al abrir el archivo en la tarjeta SD");
  }  
  //Esperamos 1 segundo para tomar o seguinte dato
  delay(1000);
  paquete++;  //Aumentamos o número de paquete en 1
  }
