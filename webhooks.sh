#! /bin/bash

STUDIO_PATH=/media/X/TD/jingxuyang/webhooks
NOW=`date +%Y%m%d%H%M%S`
CURRENT_DATE=${NOW:0:8}
CURRENT_TIME=${NOW:8:8}
APP="webhooks"

result=`ps -Af | grep python | grep ${APP}/src`

if [ -n "${result}" ]; then
    datePath=/media/X/TD/jingxuyang/webhooks/log/history/${CURRENT_DATE}

    if [ ! -d "${datePath}" ]; then
        mkdir ${datePath}
    fi

    echo "${APP} service is running\n${result}" >/media/X/TD/jingxuyang/webhooks/log/history/${CURRENT_DATE}/log_${CURRENT_TIME}.txt

else
    echo "${APP} service is down, restart it\n${result}" >/media/X/TD/jingxuyang/webhooks/log/history/${CURRENT_DATE}/log_${CURRENT_TIME}.txt

    python /media/X/TD/jingxuyang/webhooks/app.py foreground>${STUDIO_PATH}/log/log_date/log_${NOW}.txt 2>&1 &

fi