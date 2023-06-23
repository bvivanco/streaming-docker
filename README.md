# Instalacion de Spark y Kafka
El objetivo de estar instalar es contar con una cluster multinodo, con las tecnologias Spark y Kafka.

## Pre-requisitos 💡

* [Instalar Docker](https://www.docker.com/products/docker-desktop/)
  * [Video Explicativo](https://www.youtube.com/watch?v=ZO4KWQfUBBc )
* [Instalar Git](https://git-scm.com/downloads)

## Spark
* Crear cluster con docker file

    A partir del archivo [docker-compose.yml](https://github.com/bvivanco/streaming-docker/blob/main/docker-compose.yml) vamos a crear nuestro cluster.

    Abrimos un cmd y nos ubicamos donde se encuentra el archivo .yml, ejecutando este comando:

    ```bash
    docker compose -f docker-compose.yml up -d
    ```
    Esperamos unos minutos hasta que termine de crearse los contenedores de nuestro cluster.

    Abrir el siguiente link para validar la instalacion:

    [localhost:8080](http://localhost:8080/)

    ![Captura Spark](./images/capture_spark.png)

* Consultamos los contenedores creados

    Ejecutar el sgte comando:
    ```bash
    docker ps
    ```
    Resultado:
    ![Captura Lista Contenedores](./images/lista-contenedores.png)

    Nota: Seleccionar el contenedor relacionado al nodo master de Spark, el nombre que tenga `spark-master`

* Ingresar al contenedor de Spark Master
    ```bash
    docker exec -it abbf72f96045 bash
    ```

* Ejecutar un codigo python para validar nuestro cluster

    Consideracion: En la carpeta donde descargamos nuestro archivo `docker-compose.yml`, crear un archivo .py con nuestro codigo.

    ![Captura Archivos](./images/archivos.png)

    Descargar el archivo [rddexercise.py](https://github.com/bvivanco/streaming-docker/blob/main/rddexercise.py)

    Nota: Este archivo podrá ser accedido dentro de nuestro cluster, en la ruta /opt/spark

    ```bash
    I have no name!@fcf06787541f:/opt/spark$ ls -1
    docker-compose-4.yml
    otros
    proyectos
    rddexercise.py
    wordcount.py
    ```
    Asegurarnos que estemos en esta ruta `/opt/bitnami/spark`, y ejecutar el siguiente comando:
    ```bash
    spark-submit /opt/spark/rddexercise.py
    ```
    Ejemplo de la ejecucion:

    ```bash
    I have no name!@fcf06787541f:/opt/bitnami/spark$ spark-submit /opt/spark/rddexercise.py
    ```
    Finalmente, como resultado nos deberia mostrar un dataframe:
    ![Captura Resultado df](./images/resultado_df.png)