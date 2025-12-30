git

    git add . 
    git pull origin master
    git commit -m "some commit"
    git push origin master
    git rm -r --cached .

Database

    #myslq
    create database example_db character set utf8 collate utf8_unicode_ci;
    
    #postgres
    CREATE DATABASE "esi_service"
    WITH OWNER "root"
    ENCODING 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE template0;

postgres sql setting

    docker-compose exec db sh
    su - postgres -c psql
    sudo -u postgres psql //on ubuntu
    psql postgres //on mac
    CREATE USER root;
    CREATE USER root WITH PASSWORD 'harika1997';
    CREATE DATABASE djangodb OWNER postgres;
    ALTER USER postgres PASSWORD 'mynewpassword';
    ALTER DATABASE djangodb OWNER TO new_user;
    if you run project with docker so change env file DISTRIBUTOR_DB_HOST=db else DISTRIBUTOR_DB_HOST=localhost

Django

    pip3 freeze > requirements.txt.
    pip3 install -r requirements.txt
    python3 manage.py makemigrations
    python manage.py migrate

Run the collectstatic management command:

    python manage.py collectstatic

Start a Redis server on port 6379, run the following command:

    docker run -p 6379:6379 -d redis:5

To kill container

    sudo docker container ls
    sudo docker rm -f <container-name>

Run celery command:

    celery -A back worker -B -l info --concurrency=4

Run telegram bot

    python -m app.telegram_bot.bot

Run test certificate certbot

    docker-compose run --rm --entrypoint certbot certbot certonly \
      --dry-run \
      --webroot \
      --webroot-path /var/www/certbot \
      -d example.kg -d www.example.kg -d api.example.kg

Run generate certificate certbot

    docker-compose run --rm --entrypoint certbot certbot certonly \
      --webroot \
      --webroot-path /var/www/certbot \
      -d example.kg -d www.example.kg -d api.example.kg

Run renew certificate certbot

        docker-compose run --rm --entrypoint certbot certbot renew

Run certificate certbot list

        docker-compose exec certbot certbot certificates

Run cron job

    0 0 * * * docker-compose run --rm --entrypoint certbot certbot renew
    0 0 * * * cd /docker/letsencrypt-docker-nginx/src/production/project_name && docker-compose run --rm certbot renew >> /var/log/letsencrypt-renew.log 2>&1
    0 0 1 * * cd /docker/letsencrypt-docker-nginx/src/production/project_name && docker-compose run --rm --entrypoint "certbot renew --force-renewal" certbot >> /var/log/letsencrypt-renew.log 2>&1
    0 0 1 * * cd /docker/letsencrypt-docker-nginx/src/production/project_name && docker-compose run --rm certbot certbot renew --force-renewal >> /var/log/letsencrypt-renew.log 2>&1

Alembic

    alembic revision --autogenerate -m "some message"
    alembic upgrade head
    alembic downgrade -1
    alembic history --verbose
    alembic current
    alembic show <revision>
    alembic branches
    alembic merge <revision1> <revision2> -m "merge message"
    alembic stamp head

