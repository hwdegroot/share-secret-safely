run:
	docker compose --env-file ${PWD}/.env.example up


production:
	FALSK_ENV=production docker compose up

build: clean
	docker compose build

clean: stop
	sudo git clean -ffdx

stop:
	docker compose down

autoformat:
	docker compose exec app autopep8 \
		--in-place \
		--ignore E402 \
		--max-line-length 100 \
		--aggressive \
		--aggressive \
		--recursive \
		wsgi_app

lint:
	docker compose exec app autopep8 \
		--diff \
		--exit-code \
		--ignore e402 \
		--max-line-length 100 \
		--aggressive \
		--aggressive \
		--recursive wsgi_app | \
			delta --paging never --line-numbers
run-test:
	docker compose exec app nosetests test/**/*Test.py \
		--with-coverage \
		--cover-package=wsgi_app/ \
		--cover-html \
		--cover-html-dir=coverage \
		--cover-erase \
		--cover-xml \
		--cover-xml-file=junit.xml

wipe:
	docker compose down --rmi all --volumes

recreate_requirements-base:
	docker compose exec app pipenv lock -r --dev > requirements-base.txt

