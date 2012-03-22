
PYTHON=`which python`
PYTHON3=`which python3`

all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system"
	@echo "make clean - Get rid of scratch and byte files"

source:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py register sdist upload

install:
	$(PYTHON) setup.py install

install3:
	$(PYTHON3) setup.py install

install-building-packages:
	apt-get install build-essential dh-make debhelper devscripts

clean:
	$(PYTHON) setup.py clean
	rm -rf build
	find . -name '*.pyc' -delete
