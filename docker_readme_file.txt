1. execute to get the server up and running

    a) docker run --name postgres -e POSTGRES_PASSWORD="docker" -e POSTGRES_USER="postgres" -e POSTGRES_DB="database" -p 5432:5432 -d postgres

    b) alternately you can use Docker file in Database_docker folder
        and type in terminal: docker build -t postgres ./
                              docker run --name postgres -p 5432:5432 -d postgres

2. create Docker container out of Dockerfile in the main branch to get the app running

   docker build -t app ./
   docker run --name app --link postgres:postgres  -p 5432:5432 app

