dep:
	pipenv install -d

run:
	make convert

convert:
	env PIPENV_VERBOSITY=-1 pipenv run python convert_log_files.py --path data/
