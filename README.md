# Retail Sales Analysis

Cleaning, exploratory analysis and an interactive dashboard for 9,800 US retail order lines (2015–2018).

![Sales dashboard](dashboard.png)

## Key findings
- 2018 sales were $722,052, up 20.3% on 2017
- Orders rose 28.3%, while average order value fell 6.2%
- Sales are usually higher from September to December
- West was the top region and Technology the top category in 2018
- The median order line is $54, while the average is $231

## Tools
Python, pandas, seaborn, matplotlib, Streamlit, Plotly

## Data
Source: ["https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting/code"]. The data files are not included in this repository.

## Cleaning decisions
- Converted order and ship dates to date types
- Removed extra spaces in product names
- Restored leading zeros in postal codes
- Filled 11 missing Burlington, Vermont postal codes with 05401 (an assumption)
- Flagged, but kept, a possible duplicate, product ID conflicts and high sales

## Project files
- `clean_train.py`: cleans the raw data
- `eda.ipynb`: exploratory analysis
- `dashboard/app.py`: Streamlit dashboard

## How to run
1. `pip install -r requirements.txt`
2. Put `train.csv` in the project folder
3. `python clean_train.py train.csv`
4. Move `train_clean.csv` into a `data` folder
5. Open `eda.ipynb`, check the data file path, and run all cells
6. `python -m streamlit run dashboard/app.py`
