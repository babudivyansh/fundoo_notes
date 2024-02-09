ifeq ($(OS), Windows_NT)
init:
	@pip install -r requirements.txt

user:
	@uvicorn main:app --port 8000 --reload

endif
