
CMD_CREATE_PYENV := . venv/bin/activate.sh


start-app:
	gunicorn app.server:api -b 0.0.0.0:80 --workers=2 --threads=3 --keep-alive=6 -k uvicorn.workers.UvicornWorker

init-env:
	@echo "**** Starting Python Environment ****"
	$(CMD_CREATE_PYENV)