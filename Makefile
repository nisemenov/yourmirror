# DEV COMMANDS
psql:
	docker exec -it postgres psql -d telewish -U postgres

tailwind:
	python manage.py tailwind start
