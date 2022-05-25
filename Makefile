
updatefriday: randomfriday website

randomfriday: 
	python src/friday.py

website:
	python src/make_friday_page.py
	python src/make_landing_page.py