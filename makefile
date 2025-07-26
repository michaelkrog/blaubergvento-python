build:
	rm -rf build
	rm -rf blaubergvento_client.egg-info
	rm -rf dist
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build
	rm -rf blaubergvento_client.egg-info
	rm -rf dist

upload:
	twine upload --repository pypi dist/*