ps -ef | grep fast_api_server | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {}
ps -ef | grep redis | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {}
ps -ef | grep multiprocessing | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {}
nginx -s quit
