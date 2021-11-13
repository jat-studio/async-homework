current_dir = $(shell pwd)

run:
	docker run --rm -it \
        -v ${current_dir}/rabbitmq.config:/etc/rabbitmq/rabbitmq.config:ro \
        -v ${current_dir}/definitions.json:/etc/rabbitmq/definitions.json:ro \
        -p 15672:15672 -p 25672:5672 \
        rabbitmq:3.6-management
