#!/bin/bash
directorio_buscado="Piscina"
#ruta_especificada="/home/mequonic/Desktop"
ruta_especificada="/home/esteban/Desktop"
python_file_executable="Prueba_piscinas.py"


ruta_directorio="$ruta_especificada/$directorio_buscado"

if [ -d "$ruta_directorio" ]; then
    echo "Se encontró el directorio '$directorio_buscado' en la ruta '$ruta_especificada'."
    # Haz algo si el directorio existe
    # ... añade aquí la rutina que deseas ejecutar
    cd $ruta_directorio
    #cd /home/mequonic/Desktop/Piscina
    #Reset all the chages done of the git
    git reset --hard
    #Pull the latest changes of the git
    git pull
    #Goes to the main branch
    git checkout main
    cd GUI
    chmod +x $python_file_executable
    python3 $python_file_executable
    read


else
    echo "No se encontró el directorio '$directorio_buscado' en la ruta '$ruta_especificada'."
    # Haz algo si el directorio no existe
    # ... añade aquí la otra rutina que deseas ejecutar
    git clone https://github.com/estebandsilva/Piscina

fi
