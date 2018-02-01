# vim: set ts=4 sw=4 noet:

VERSION=v1.0.0
REPO=pm01

.DEFAULT_GOAL := all

test:
	SETTINGS='test' PYTHONPATH='src' python -m unittest discover -s tests -v

minikube:
	eval $$(minikube docker-env) && docker build -t $(REPO):$(VERSION) .
	eval $$(minikube docker-env) && docker tag $(REPO):$(VERSION) $(REPO):latest
	kubectl apply -f $(REPO).yaml
	kubectl expose deployment $(REPO) --type=LoadBalancer | echo 'Service already exists'
	echo 'SERVICE ENDPOINT:'
	minikube service --url $(REPO)

delete:
	kubectl delete service $(REPO)
	kubectl delete -f $(REPO).yaml

.PHONY: minikube test delete

all: test minikube
