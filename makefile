
all: install exe

exe:
	python3 -B ./src/netperf.py

install:
	python3 -m pip install pingparsing
	python3 -m pip install matplotlib
	python3 -m pip install numpy
