sudo service docker start
sudo docker compose build
sudo docker compose up -d --force-recreate
pip install -e .
alembic upgrade heads
