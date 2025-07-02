set -x

export TERM=dumb

./redis-7.2.7/src/redis-server ./redis-7.2.7/redis.conf &

uvicorn fast_api_server:app --host 0.0.0.0 --port 12345 --workers 16
