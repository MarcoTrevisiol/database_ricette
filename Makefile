target=

all_docker: docker_image_bot docker_image_web docker_image_backup

docker_image_bot:
	docker build -t ricette_personali_bot telegram_bot/

docker_image_web:
	cd web_ui && make clean && make
	docker build -t sito_ricette web_ui/

docker_image_backup:
	docker build -t backup backup/

remote_prepare:
	rsync -av docker_preparation.sh docker-compose.yml ${target}
