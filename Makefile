TAG := registry.gitlab.com/hwdegroot/secret-sharing:python-3.9

run: build
	docker-compose up

build: clean
	docker-compose build

clean: stop
	git clean -ffdx

stop:
	docker-compose down

wipe:
	docker-compose down --rmi all --volumes

create_docker: build
	docker build -t registry.gitlab.com/hwdegroot/secret-sharing . && \
	docker push registry.gitlab.com/hwdegroot/secret-sharing

