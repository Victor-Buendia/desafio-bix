.PHONY: help
help:
	@echo "****************** COMMANDS  ***********************"
	@echo 
	@echo "deploy: Inicializa todos os containers e deixa o data pipeline funcional"
	@echo "env-check: Configura um template do arquivo .env"
	@echo
	@echo "clear: Para e deleta todos os containers junto com seus volumes"
	@echo "build: Builda todas as imagens para os containers"
	@echo "up: Sobe os containers Docker"
	@echo
	@echo "***************************************************"

.PHONY: clear
clear:
	docker-compose rm -fsv

.PHONY: deploy
deploy: env-check build up
env-check:
	chmod +x env_check.sh
	sh ./env_check.sh
build:
	docker-compose down && docker-compose build
up:
	docker-compose up