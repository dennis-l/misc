'''
    friday.py
    ~~~~~~~~~
'''

import logging
import numpy as np

minute_value = int(np.random.rand() * 60)

logging.basicConfig(
    filename="data/friday.log", 
    filemode='a',
	format='%(asctime)s | %(message)s',
	datefmt="%Y-%m-%d %H:%M:%S",
	level=logging.INFO
)

logging.info(f"np.random.rand() * 60 | <mark>4:{minute_value:02d} PM</mark>")
