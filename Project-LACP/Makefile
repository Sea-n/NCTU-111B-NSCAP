run:
	docker exec -it lacp-send-1 /send.sh

new:
	make clean
	docker compose up -d --build
	make run

clean:
	docker compose kill --remove-orphans
	docker compose rm -sf
	docker network rm $$(docker network ls -q -f name=lacp)
