dev-file=docker-compose.dev.yaml

.SILENT:
.ONESHELL:
.PHONY: tests

init: run make-dataset

run:
	@echo "Running data transformation..."
	poetry run transform-datatourisme || exit 1
	@echo "Starting Docker containers..."
	docker compose up
down:
	docker compose down

clean:
	docker compose down
	docker image rm holiday-internal-ui:latest neo4j-api:latest
	docker volume rm neo4j_data


## Development
create-dataset:
	poetry run transform-datatourisme
	docker compose up neo4j neo4j-post-init --abort-on-container-exit

run-dev:
	docker compose -f ${dev-file} up

down-dev:
	docker compose -f ${dev-file} down

clean-dev:
	docker compose -f ${dev-file} down
	docker image rm holiday-internal-ui:dev neo4j-api:dev
	docker volume rm neo4j_data_dev

run-airflow:
	docker compose -f docker-compose.airflow.yaml up

down-airflow:
	docker compose -f docker-compose.airflow.yaml down

tests:
	docker build --target development -t ui-tests:dev . || exit 1
	docker run -it \
		--network testnet \
		-e NEO4J_URI=bolt://neo4j-test:7687 \
		-e NEO4J_USER=neo4j \
		-e NEO4J_PASSPHRASE="" \
		ui-tests:dev
	docker rmi ui-tests:dev
	docker rm -f neo4j-test
