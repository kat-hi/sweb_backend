run:
	flask run

docker_build:
	sudo docker build -t registry.datexis.com/ksachs/sweb-server .

docker_push:
	sudo docker push registry.datexis.com/ksachs/sweb-server

docker_run:
	sudo docker run registry.datexis.com/ksachs/sweb-server

