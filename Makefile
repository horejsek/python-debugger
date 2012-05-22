
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

test:
	$(PYTHON) tests/allTests.py

localdev:
	cp git-hooks/* .git/hooks/
	chmod 755 .git/hooks/

clean:
	$(PYTHON) setup.py clean
	rm -rf build
	find . -name '*.pyc' -delete
