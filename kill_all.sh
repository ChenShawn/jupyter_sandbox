ps -ef | grep fast_api_server | awk '{print $2}' | xargs -I {} kill -9 {}
nginx -s quit
ps -ef | grep redis | awk '{print $2}' | xargs -I {} kill -9 {}
