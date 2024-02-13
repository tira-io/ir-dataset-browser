build-ui-docker:
	docker run --rm -v ${PWD}:/app -v ${PWD}/static/dist/:/dist -w /app/ui --entrypoint vite mam10eks/github-page-tutorial:0.0.2 build

indexer-bash:
	docker run --rm -ti -v /mnt/ceph/storage/data-tmp/current/kibi9872/ir-dataset-browser:/app \
		-v /mnt/ceph/tira/state/ir_datasets/:/root/.ir_datasets:ro \
		-v /mnt/ceph/storage/data-tmp/current/kibi9872/.tira:/root/.tira \
		--entrypoint bash \
		-w /app \
		mam10eks/github-page-tutorial:0.0.2

coverage:
	 pytest --cov=construct_indices \
	 && coverage-badge -o construct_indices/coverage.svg
