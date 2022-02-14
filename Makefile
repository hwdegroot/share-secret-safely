TAG := registry.gitlab.com/hwdegroot/secret-sharing:python-3.9

run: build
	docker-compose up

build: clean
	docker-compose build

clean: stop
	git clean -ffdx

stop:
	docker-compose down

autoformat:
	docker-compose exec app autopep8 \
		--in-place \
		--ignore E402 \
		--max-line-length 100 \
		--aggressive \
		--aggressive \
		--recursive \
		wsgi_app

run_test:
	docker-compose exec app python wsgi_app/test/run_tests.py

wipe:
	docker-compose down --rmi all --volumes

create_docker: build
	docker build -t registry.gitlab.com/hwdegroot/secret-sharing . && \
	docker push registry.gitlab.com/hwdegroot/secret-sharing

