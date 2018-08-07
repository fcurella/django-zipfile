test:
	python setup.py test

clean:
	rm -rf build dist

build: clean
	python setup.py sdist bdist_wheel

release: build
	twine upload dist/*
