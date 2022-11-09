.PHONY: all
all: ami

WBDV_VERSION = whiting-lab

wave-big-data-visualizer:
	(mkdir tmp.clone && \
	 cd tmp.clone && \
	 git clone https://github.com/h2oai/wave-big-data-visualizer && \
	 cd wave-big-data-visualizer && \
	 git checkout $(WBDV_VERSION))
	cp -rp tmp.clone/wave-big-data-visualizer .
	rm -rf tmp.clone

wave-apps:
	(mkdir tmp.clone && \
	 cd tmp.clone && \
	 git clone https://github.com/h2oai/wave-apps)
	cp -rp tmp.clone/wave-apps .
	rm -rf tmp.clone

.PHONY: docker-image-only
docker-image-only: 
	docker build . -t wave-aquarium-lab

.PHONY: docker-image
docker-image: wave-big-data-visualizer wave-apps docker-image-only

wave-aquarium-lab.tar.gz-only:
	docker save wave-aquarium-lab | pigz > $@.tmp
	mv $@.tmp $@

wave-aquarium-lab.tar.gz: docker-image wave-aquarium-lab.tar.gz-only

.PHONY: ami-only
ami: 
	export AWS_REGION=us-west-2
	packer build .

.PHONY: ami
ami: wave-aquarium-lab.tar.gz ami-only

.PHONY: clean
clean:
	-docker rmi wave-aquarium-lab
	rm -rf tmp.clone
	rm -rf wave-big-data-visualizer
	rm -rf wave-apps
	rm -f wave-aquarium-lab.tar.gz
