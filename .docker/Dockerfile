FROM python:3.8


ENV WORK_DIR /var/www/kitoboy_service/backend
ENV GECKODRIVER_VER v0.24.0
ENV FIREFOX_VER 87.0


# Install base packages
RUN apt-get update && apt-get install -y \
  firefox-esr \
  libpq-dev \
  apt-utils \
  gcc \
  curl \
  nano \
  nginx \
  python3-setuptools \
  python3-pip \
  locales \
  libpcre3-dev \
  uwsgi \
  uwsgi-plugin-python3 \
  libpcre3 \
  python3-wheel \
  libssl-dev \
  supervisor \
  systemd && \
  echo "daemon off;" >> /etc/nginx/nginx.conf && \
  echo "export PYTHONPATH=$WORK_DIR" >> /root/.bashrc && \
  mkdir -p $WORK_DIR



# Add FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar -xvzf geckodriver* \
   && chmod +x geckodriver \
   && mv geckodriver /usr/bin/



COPY . $WORK_DIR


# creates log files for celery, add celery user, creates nginx.conf, creates supervisord.conf
RUN  touch  celery_tasks-stderr.log  celery_tasks-stdout.log && \
     useradd celery && \
     # chmod 666 $WORK_DIR/app/logs/* && \
     # cp $WORK_DIR/nginx.conf /etc/nginx/sites-available/default && \
     # cp $WORK_DIR/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
     chmod u+x $WORK_DIR/scripts/db_fill.sh


RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache  -r $WORK_DIR/requirements.txt && \
    python3.8 -m dostoevsky download fasttext-social-network-model


WORKDIR $WORK_DIR

ARG app_version=0.0.0
ENV APP_VERSION=${app_version}


CMD ["gunicorn",  "-b", "0.0.0.0:8000",  "main:app"]
