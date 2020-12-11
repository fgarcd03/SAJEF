#!/bin/bash

#Este programa instala las dependencias necesarias de python para ejecutar el programa. Debería funciona para Ubuntu 20.04 y derivadas. Necesita permiso de root para instalar algunos de los paquetes.

echo "Espere a que se instale las dependencias necesarias para ejecutar el programa."

pkexec bash -c "apt install python3 python3-pip -y;apt install --reinstall libxcb-xinerama0 -y"
pip3 install pyqt5 matplotlib neo4j

echo "Hecho, instalación de dependencias completada con exito, ya puede cerrar esta ventana"
