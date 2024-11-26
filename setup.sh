docker network create flyway-network
docker run --name postgres-db --network flyway-network -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
docker run -it --rm --name flyway --network flyway-network -v "$PWD"/migrations:/flyway/sql -e FLYWAY_URL=jdbc:postgresql://postgres-db:5432/postgres -e FLYWAY_USER=postgres -e FLYWAY_PASSWORD=password flyway/flyway migrate