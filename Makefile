help:
	@echo '                                                                                             '
	@echo 'Makefile for the recipe_service                                                              '
	@echo '                                                                                             '
	@echo 'Usage:                                                                                       '
	@echo '    make run                       run service                                               '
	@echo '    make test                      run tests                                                 '
	@echo '    make compose                   build and launch container                                '
	@echo '                                                                                             '

run:
	python ./src/

test:
	pytest --cov-report term-missing --cov=. -vvv

compose:
	docker-compose up -d --build