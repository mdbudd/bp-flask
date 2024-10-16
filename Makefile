IMAGE_NAME := flask
TAG ?= latest

flask:
	make compose

compose:
	docker compose up

recompose:
	docker compose up --build

into:
	docker exec -it python sh

jupyter:
	docker exec -it flask jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

unit_test:
	docker exec -it flask python /python/flask/tests.py

jmeter_build:
	docker build --no-cache -t jmeter_base:latest -f docker/jmeter/Dockerfile .

# Add NAME of test when calling
jmeter_test:
	docker run -it -d --name jmeter jmeter_base:latest
	docker cp ./jmeter/tests jmeter:/opt/apache-jmeter-5.3/bin
	docker exec -it jmeter bash -c "cd bin; sh jmeter -n -t tests/$(NAME).jmx -JThreadNumber=10 -JRampUpPeriod=1 -Jiterations=10 -l results.csv -e -o /gui_output"
	docker cp jmeter:/gui_output ./jmeter/tests/gui_output/$(NAME)/
	docker stop jmeter
	docker rm jmeter

jmeter_ui:
	docker build -t jmeter_ui:latest -f ./docker/jmeter/Dockerfile.ui .

run_gui:
	docker run -v ${PWD}/jmeter/tests:/home/alpine/tests -e PASSWD=pword -d -p 5900:5900 --name jmeter_ui jmeter_ui:latest

# Add NAME of test when calling
non_gui:
	docker run -v ${PWD}/jmeter/tests:/home/alpine/tests --name jmeter_noui jmeter_ui:latest jmeter -n -t tests/$(NAME).jmx -l tests/nogui_output/$(NAME)/results.jtl
	docker stop jmeter_noui
	docker rm jmeter_noui
	
lint:
	cd python
	isort ./
	black --line-length=80 ./
	flake8 ./
	# mypy --ignore-missing-imports ./