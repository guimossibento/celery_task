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
 
docker build -t registry.gitlab.com/mtvp/celery_task .
docker push registry.gitlab.com/mtvp/celery_task
 
docker stack rm celery_stack
docker pull registry.gitlab.com/mtvp/celery_task
docker stack deploy -c docker-compose.yml celery_stack
docker service scale celery_stack_worker=2
 
docker ps
docker exec -it d4ca37349339 python3 /app/trigger_task_integrity_save_each_time.py
docker exec -it 805a54896bdc python3 /app/trigger_task_integrity_save_lot.py
docker exec -it 805a54896bdc python3 /app/trigger_task_integrity_save_lot_chunk.py

docker network create -d bridge celery_task  

docker service logs celery_stack_worker -f 
 
docker build -t localhost:5000/celery_worker:latest .
docker push localhost:5000/celery_worker:latest   
````