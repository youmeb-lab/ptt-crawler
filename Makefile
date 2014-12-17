PM := python_modules
CMD := docker run --rm -it -w /app -v $(shell pwd):/app \
	-e PYTHONPATH=/app/$(PM)/lib/python3.4/site-packages python:3.4.2

ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

init:
	@mkdir -p $(PM)
	@$(CMD) pip install --install-option="--prefix=/app/$(PM)" -r ./requirements-dev.txt

pip:
	@$(CMD) pip $(ARGS)

bash:
	@$(CMD) bash $(ARGS)

python:
	@$(CMD) python $(ARGS)

command:
	@$(CMD) $(ARGS)

lint:
	@flake8 pttparser
