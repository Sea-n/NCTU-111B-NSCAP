clean:
	docker compose kill --remove-orphans
	docker compose rm -sf
	docker network rm $$(docker network ls -q -f name=lacp)
