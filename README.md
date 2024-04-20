# Python Data Analysis Project

This project focuses on data analysis and visualization using Python, specifically leveraging libraries such as Pandas, Matplotlib, and SQLAlchemy for database operations. The repository includes scripts for loading data from CSV files into an SQLite database, analyzing this data, and visualizing the results.

## Project Structure

- `load_data.py`: Script to load data into an SQLite database.
- `select_ideal_functions.py`: Contains functions to select the most ideal data points from the dataset based on certain criteria.
- `map_test_data.py`: Maps test data to selected ideal functions.
- `data_visualization.py`: Contains functions to plot training, test, and ideal function data.
- `tests/`: Contains unit tests for data processing functions.

## Setup

### Requirements

This project requires Python 3.x. All dependencies can be installed via pip:

```bash
pip install pandas matplotlib sqlalchemy
