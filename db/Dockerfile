# Create from official mysql image
FROM mysql:8.0

# Add a database
ENV MYSQL_DATABASE posterr

# Initial db scripts
COPY ./init-scripts /docker-entrypoint-initdb.d/