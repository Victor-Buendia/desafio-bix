.PHONY: help
help:
	@echo "****************** COMMANDS  ***********************"
	@echo
	@echo "deploy: Inicializa todos os containers e deixa o data pipeline funcional"
	@echo
	@echo "***************************************************"

.PHONY: deploy
deploy: os-check build up
os-check:
	chmod +x linux_patch.sh
	sh ./linux_patch.sh
build:
	docker-compose down && docker-compose build && docker-compose up -d
up:
	docker-compose up