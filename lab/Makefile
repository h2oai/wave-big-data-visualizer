all: build

WBDV_VERSION = tomk-lab

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

build: wave-big-data-visualizer wave-apps
	docker build . -t wave-lab

clean:
	rm -rf wave-big-data-visualizer
	rm -rf wave-apps
