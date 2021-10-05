# Instrucciones de uso

1. Descargue el repositorio en la máquina cliente y la máquina servidor. Navegue a la carpeta del repositorio.

2. Tanto el programa del servidor como el de los clientes hacen uso de una utilidad de red llamada `Tcpdump`, que viene incluida por defecto en computadores Unix (como MacOS y Linux). Si va a ejecutar algún programa en una máquina Windows, puede instalar un clon de Tcpdump para Windows (https://www.microolap.com/products/network/tcpdump/).

3. Instale el módulo `scapy` en Python.
```
pip install scapy
```

4. Escoja el archivo que va a transmitir o genere un archivo aleatorio del tamaño fijo deseado. El nombre del archivo debe ser de 7 caracteres, incluyendo al punto y la extensión. El comando en MacOS/Linux para crear un archivo aleatorio de 100 MB sería el siguiente:
```
fallocate -l 100M 123.txt
```

5. En el código .py de ambos programas (servidor y clientes), cambie el valor de los parámetros `SERVER_IP` y `SERVER_PORT` para que coincidan con la dirección IP de su máquina servidor y con el puerto del servidor en donde quiere que se preste el servicio. Para ambos parámetros, su valor debería coincidir en el código del cliente y en el código servidor. Así mismo, ingrese el nombre de la interfaz de red por la que se conectarán servidor y clientes en el parámetro `INTERFACE`. El valor para la interfaz, con seguridad, si será diferente en la máquina servidor y en la máquina cliente. A continuación se muestra un ejemplo:
```
INTERFACE = "en0"
SERVER_IP = "192.168.1.155"
SERVER_PORT = 9090
```

6. Ejecute el programa `server.py` en la máquina del servidor. Como parámetros de entrada, se debe indicar la cantidad de clientes y el archivo a transmitir. Es totalmente necesario ejecutar el programa como administrador (`sudo` en MacOS/Linux). El comando para ejecutar el programa con 10 clientes y un archivo llamado 123.txt sería el siguiente:
```
sudo python server.py 10 123.txt
```

6. Después de haber dejado iniciado el programa del servidor, se debe ejecutar el programa `clients.py` en la máquina cliente. Como parámetro de entrada, se debe indicar la cantidad de clientes (cuyo valor debería coincidir con lo indicado al servidor en el punto anterior). Es totalmente necesario ejecutar el programa como administrador (`sudo` en MacOS/Linux). El comando para ejecutar el programa con 10 clientes sería el siguiente:
```
sudo python clients.py 10
```

7. El programa cliente va a imprimir en consola el estado de los clientes. El programa servidor no va a imprimir nada. Finalizada la transferencia de archivos a todos los clientes, ambos programas van a terminar y en cada máquina quedará una carpeta `/Logs` con los registros de conexiones. Adicionalmente, en la máquina cliente habrá una carpeta `/ArchivosRecibidos` que tiene almacenados los archivos recibidos durante la transferencia.
