doc:
	pandoc --from=markdown --to=rst --output="README.rst" "README.md"

clean:
	rm dist/* || true
	rm -fr __pycache__ || true
	rm -fr fileperms/__pycache__ || true
	rm -fr build || true

build:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

upload:
	twine upload dist/fileperms*

distro: clean build upload
