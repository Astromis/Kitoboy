FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV WORK_DIR /var/www/kitoboy/backend

# Install base packages
RUN apt-get update && apt-get install -y \
  libpq-dev \
  apt-utils \
  gcc \
  curl \
  nano \
  nginx \
  python3.8 \
  libpython3.8 \
  python3.8-dev \
  python3.8-venv \
  python3-setuptools \
  python3-pip \
  locales \
  libpcre3-dev \
  uwsgi \
  uwsgi-plugin-python3 \
  libpcre3 \
  python-wheel \
  libssl-dev \
  supervisor \
  systemd && \
  echo "daemon off;" >> /etc/nginx/nginx.conf && \
  echo "export PYTHONPATH=$WORK_DIR" >> /root/.bashrc && \
  mkdir -p $WORK_DIR


COPY . $WORK_DIR


# creates log files for celery, add celery user, creates nginx.conf, creates supervisord.conf
RUN  touch  celery_tasks-stderr.log  celery_tasks-stdout.log && \
     useradd celery && \
     # chmod 666 $WORK_DIR/app/logs/* && \
     cp $WORK_DIR/nginx.conf /etc/nginx/sites-available/default && \
     cp $WORK_DIR/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
     chmod u+x $WORK_DIR/scripts/db_fill.sh


RUN pip3 install --no-cache  -r $WORK_DIR/requirements.txt

WORKDIR $WORK_DIR

ARG app_version=0.0.0
ENV APP_VERSION=${app_version}


# CMD ["/usr/bin/supervisord"]
CMD ["python3", "main_2.py", "runserver"]
