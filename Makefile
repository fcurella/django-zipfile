test:
	python django_zipfile/tests/runtests.py

release:
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload dist/*