dep:
	pipenv install -d

run:
	make convert

convert:
	pipenv run python -m converter.converter
