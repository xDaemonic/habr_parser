upload:
	 git add -A && git commit -m "local upload $(date '+%Y-%m-%d %H:%M:%S')" && git pull && git push
	
dde:
	docker compose down

dup:
	docker compose up -d

dbb:
	docker compose build

rvol:
	docker volume remove habr_pg_db && docker volume create habr_pg_db

pb:
	docker exec -it habr_parser sh

pdb:
	docker exec -it habr_parser_db bash