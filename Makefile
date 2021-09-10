clean:
	black .
	isort --profile=black .

elastic:
	git submodule update --recursive --remote
	docker compose -f compose-recipes/elastic/compose.yml up -d
	@echo it will take a bit for elasticsearch to be ready


test-stdout:
	LOG_LEVEL=info NED_AMOUNT_RECORDS=1 poetry run ned --type=netflow

test-elastic:
	LOG_LEVEL=info NED_AMOUNT_RECORDS=100 NED_AMOUNT_RECORDS_ANOMALOUS=5 poetry run ned --type netflow --to-elastic

build:
	docker build -t ned:dev .

test-docker: build
	docker run -it -e LOG_LEVEL=critical -e NED_AMOUNT_RECORDS=1 ned:dev --type netflow

test-docker-elastic:
	docker run -it -e LOG_LEVEL=info -e ES_HOST=host.docker.internal -e NED_AMOUNT_RECORDS=1 ned:dev --type netflow --to-elastic

test-compose-elastic:
	docker compose -f deployment/docker-compose.yml -f deployment/dev.yml up

deployment: config-bootstrap
	docker compose -f deployment/docker-compose.yml -f deployment/prod.yml up -d

deployment-linux: config-bootsrap
	@echo $$IP_ADDRESS
	docker compose -f deployment/docker-compose.yml -f deployment/prod.yml -f deployment/linux.yml up -d

config-bootstrap:
	export IP_ADDRESS=$$(ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1)
	@if $(MAKE) -s confirm ; then \
		cp deployment/config-defaults.env deployment/config.env ; \
		nano deployment/config.env ; \
	fi

# The CI environment variable can be set to a non-empty string,
# it'll bypass this command that will "return true", as a "yes" answer.
confirm:
	@if [[ -z "$(CI)" ]]; then \
		REPLY="" ; \
		read -p "⚠ This will erase the content of deployment/config.env. Are you sure? [y/n] > " -r ; \
		if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
			printf $(_ERROR) "KO" "Stopping" ; \
			exit 1 ; \
		else \
			printf $(_TITLE) "OK" "Continuing" ; \
			exit 0; \
		fi \
	fi
.PHONY: confirm
_TITLE := "\033[32m[%s]\033[0m %s\n" # Green text for "printf"
_ERROR := "\033[31m[%s]\033[0m %s\n" # Red text for "printf"
