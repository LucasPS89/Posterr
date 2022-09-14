# Create from official mysql image
FROM mysql:5.7

# Add a database
ENV MYSQL_DATABASE testdb

# Initial db scripts
COPY ./init-scripts /docker-entrypoint-initdb.d/