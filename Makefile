clean:
	black .
	isort --profile=black .

elastic:
	docker compose -f compose-recipes/elastic/compose.yml up -d

test-stdout:
	LOG_LEVEL=info AMOUNT_RECORDS=1 poetry run ned --type=netflow

test-elastic:
	LOG_LEVEL=info AMOUNT_RECORDS=100 AMOUNT_ANOMALOUS=5 poetry run ned --type netflow --to-elastic
