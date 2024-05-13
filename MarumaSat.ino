//Librerías que necesitamos
#include <Wire.h>
#include <SPI.h>
#include <SD.h>

#define SSpin 10  //Módulo microSD conectado ao pin 10


int paquete = 0;// Variable para identificar o número de paquete enviado.
float peltier, V_peltier;  //un float é un número con decimais (6 ou 7 decimais).

File logFile;  //Variable para o nome dos datos na SD.

void setup() {
  pinMode(A0, INPUT);  //Pin para a lectura da Voltaxe Peltier

  Serial.begin(9600);

 
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
  peltier = analogRead(A0);             //lectura da Voltaxe peltier
  V_peltier = peltier / 1023 * 5.0;

  //Imprimimos identificador do Cansat (Muxia) e o número de paquete e enviámolas ao receptor do APC220
  Serial.println(V_peltier, 3);

  //Gardamos os datos na SD
  logFile = SD.open("datos.txt", FILE_WRITE);
  if (logFile) {
    logFile.print(paquete);
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
