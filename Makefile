
updatefriday: randomfriday website

randomfriday:
	python src/friday.py

calibrator:
	python src/make_calibrator_page.py
	python src/make_nopol_page.py
	python src/make_landing_page.py

website:
	python src/make_friday_page.py
	python src/make_landing_page.py

rebuild:
	python src/make_calibrator_page.py
	python src/make_friday_page.py
	python src/make_landing_page.py
	python src/make_nopol_page.py
