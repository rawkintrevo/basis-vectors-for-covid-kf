FROM gcr.io/spark-operator/spark:v2.4.5
COPY target/covid-0.1-jar-with-dependencies.jar /

CMD mkdir data

ENTRYPOINT ["/opt/entrypoint.sh"]
