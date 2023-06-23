# Instalacion de Spark y Kafka
El objetivo de estar instalar es contar con una cluster multinodo, con las tecnologias Spark y Kafka.

## Pre-requisitos 💡

* [Instalar Docker](https://www.docker.com/products/docker-desktop/)
  * [Video Explicativo](https://www.youtube.com/watch?v=ZO4KWQfUBBc )
* [Instalar Git](https://git-scm.com/downloads)

## Spark
* Crear cluster con docker file

    A partir del archivo "docker-compose.yml" vamos a crear nuestro cluster.

    Abrimos un cmd y nos ubicamos donde se encuentra el archivo .yml, ejecutando este comando:

    ```bash
    docker compose -f "myfile.yml" up -d
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

    Nota: Seleccionar el contenedor relacionado al nodo master de Spark, el nombre que tenga `spark-1`

* Ingresar al contenedor de Spark Master
    ```bash
    docker exec -it fcf06787541f bash
    ```

* Ejecutar un codigo python para validar nuestro cluster

    Consideracion: En el lugar donde dejamos nuestro archivo `docker-compose.yml`, crear un archivo .py con nuestro codigo.

    ![Captura Archivos](./images/archivos.png)

    Descargar el archivo [rddexercise.py](https://github.com/bvivanco/streaming-docker/blob/main/rddexercise.py)

    ```bash
    spark-submit /opt/spark/rddexercise.py
    ```
    Asegurarnos que estemos en esta ruta `/opt/spark`, ejemplo de ejecucion final:

    ```bash
    I have no name!@fcf06787541f:/opt/bitnami/spark$ spark-submit /opt/spark/rddexercise.py
    ```
    Finalmente, como resultado nos deberia mostrar un dataframe:
    ![Captura Resultado df](./images/resultado_df.png)
    
