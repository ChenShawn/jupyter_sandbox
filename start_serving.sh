set -x

export TERM=dumb

mkdir -p uvilog
./redis-7.2.7/src/redis-server ./redis-7.2.7/redis.conf >./uvilog/redis.log 2>&1 &

uvicorn fast_api_server:app --host 0.0.0.0 --port 18901 --workers 8 >./uvilog/uv1.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18902 --workers 8 >./uvilog/uv2.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18903 --workers 8 >./uvilog/uv3.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18904 --workers 8 >./uvilog/uv4.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18905 --workers 8 >./uvilog/uv5.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18906 --workers 8 >./uvilog/uv6.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18907 --workers 8 >./uvilog/uv7.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18908 --workers 8 >./uvilog/uv8.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18909 --workers 8 >./uvilog/uv9.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18910 --workers 8 >./uvilog/uv10.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18911 --workers 8 >./uvilog/uv11.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18912 --workers 8 >./uvilog/uv12.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18913 --workers 8 >./uvilog/uv13.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18914 --workers 8 >./uvilog/uv14.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18915 --workers 8 >./uvilog/uv15.log 2>&1 &
uvicorn fast_api_server:app --host 0.0.0.0 --port 18916 --workers 8 >./uvilog/uv16.log 2>&1 &

nginx -c `pwd`/nginx.conf
wait
