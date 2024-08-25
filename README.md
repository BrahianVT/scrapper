# scrapper
Python scrapper that allows you to fill in a csv file with the results of searching cars in sale that are published in Facebook market place 

## How it works...
It uses splinter with selenium to control the webbrowser by using Chromedriver.
The is go straigth in to the facebook marketplace search url "https://www.facebook.com/marketplace/mexicocity/search?", the search can be tunned by adding multiple in-url parameters such as:
- min_price : int val
- max_price : int val
- days_listed : int val
- min_mileage : int val
- max_mileage : int val
- min_year : int val
- max_year : int val
- transmission : string val
- make = string val
- model = string val

After getting the results page, it scrolls a few times, get the page plain.html parse it using beautifulsoup and searches for each result tile and stores it title, link, location and price.
Finally adds every entry to a dataframe and exports it in a csv file

## Usage
1. Check the installed version of your chrome web browser, and the intall the compatible chromedriver for it. Make sure to add the chromedriver executable in the PATH.
1. Install the required python packages using pip:
```
pip install -r requirements.txt
```
1. Run the script and a file named `carros.csv` will be created with the found results.
