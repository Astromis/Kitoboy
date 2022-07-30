#!/bin/bash
# Принимает 1 ключ с указанием режима работы докера:
# dev или prod
# запускать: ./db_fill.sh dev   (или прод)

if [ "$1" ]
then
  mode="$1"
  python3.8 $WORK_DIR/db_manager.py create_digital_users -f $WORK_DIR/data_for_db/digital_user.json
  python3.8 $WORK_DIR/db_manager.py create_posts
  echo Done



else
  echo there\'s no argument
fi

