build-ui-docker:
	docker run --rm -ti -v ${PWD}:/app -v ${PWD}/static/dist/:/dist -w /app/ui --entrypoint vite mam10eks/github-page-tutorial:0.0.1 build
