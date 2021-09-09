clean:
	black .
	isort --profile=black .

elastic:
	docker compose -f compose-recipes/elastic/compose.yml up -d

test:
	LOG_LEVEL=info poetry run ned --type netflow --to-elastic
