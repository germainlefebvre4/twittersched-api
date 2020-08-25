build:
	docker build -t g/bspauto-batch .

run:
	docker stop bspauto-batch || true
	docker rm bspauto-batch || true
	docker run -tid --name=bspauto-batch g/bspauto-batch

exec:
	docker exec -ti bspauto-batch bash

logs:
	docker logs bspauto-batch
