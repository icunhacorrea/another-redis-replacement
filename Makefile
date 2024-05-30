
perf:
	docker run --network host -it --rm redis:alpine redis-benchmark	-t set,get, -n 10000 -p 7070

perf-redis:
	docker run --network host -it --rm redis:alpine redis-benchmark	-t set, -n 10000 -p 6379

cli:
	docker run --network host -it --rm redis:alpine redis-cli -p 7070

run-redis:
	docker run -d \
		--rm \
		--hostname=redis \
		--network=host \
		--name redis \
		redis:alpine

stop-redis:
	docker stop redis
