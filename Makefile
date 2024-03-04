.PHONY: help
help:
	@echo "****************** COMMANDS  ***********************"
	@echo
	@echo "deploy: Inicializa todos os containers e deixa o data pipeline funcional"
	@echo
	@echo "***************************************************"

.PHONY: deploy
deploy: build up
build:
	docker-compose down && docker-compose build && docker-compose up -d
up:
	docker-compose up