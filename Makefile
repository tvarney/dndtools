.PHONY: clean
clean:
	rm -rf __pycache__ **/__pycache__ *.pyc **/*.pyc

.PHONY: format
format:
	black *.py dnd/*.py

