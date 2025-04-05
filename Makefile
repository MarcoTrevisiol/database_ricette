target=
platform=linux/arm/v7
tag=:arm
IMAGES=telegram_bot web_ui
DOCKER_IMAGES=$(patsubst %, docker_image_%.tar, $(IMAGES))

all_docker: $(DOCKER_IMAGES)

$(DOCKER_IMAGES): docker_image_%.tar: %
	docker buildx build --platform ${platform} -t $<${tag} $</
	docker save $<${tag} > $@

docker_image_web_ui: web_ui_preparation
web_ui_preparation:
	cd web_ui && make clean && make

remote_prepare: $(DOCKER_IMAGES)
	rsync -avP docker_preparation.sh docker-compose.yml $^ ${target}

clean:
	-rm $(DOCKER_IMAGES)
