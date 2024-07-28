# celery_task


````
cur.execute('''
    CREATE TABLE IF NOT EXISTS sequences (
        id SERIAL PRIMARY KEY,
        number INTEGER,
        sqrt_value FLOAT,
        task_type VARCHAR(255),
        task_number INTEGER
    )
''')

git pull origin master
 
docker stack rm celery_stack
 
docker build -t localhost:5000/celery_worker:latest .
docker push localhost:5000/celery_worker:latest

docker stack deploy -c docker-compose.yml celery_stack

docker ps
docker exec -it afd4e37edab4 python3 /app/trigger_task_integrity_save_each_time.py
docker exec -it 9dfcaefd5f27 python3 /app/trigger_task_integrity_save_lot.py
docker exec -it d68ab848c34a python3 /app/trigger_task_integrity_save_lot_chuck.py
````