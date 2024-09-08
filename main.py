from splinter import Browser
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time
import urllib


def scrap():
    # Use a breakpoint in the code line below to debug your script.
    # Set up Splinter
    browser = Browser('chrome')
    # Set up base url
    base_url = "https://www.facebook.com/marketplace/mexicocity/search?"
    # Set up search parameters
    min_price = 40000
    max_price = 100000
    min_year = 2005
    max_year = 2010
    transmission = "manual"
    make = "ford"
    model = "ranger"
    searchQuery =  urllib.parse.quote(f'{make} {model}')
    # Set up full url
    #url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_listed}&maxMileage={max_mileage}&maxYear={max_year}&minMileage={min_mileage}&minYear={min_year}&transmissionType={transmission}&query={make}{model}&exact=false"
    url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&maxYear={max_year}&minYear={min_year}&transmissionType={transmission}&query={searchQuery}&exact=false"

    print("Checking at URL ")
    print(url)
    # Visit the website
    
    browser.visit(url)
    if browser.is_element_present_by_css('div[aria-label="Close"]', wait_time=5):
        # Click on the element once it's found
        browser.find_by_css('div[aria-label="Close"]').first.click()

    # Scroll down to load more results

    # Define the number of times to scroll the page
    scroll_count = 10
    # Define the delay (in seconds) between each scroll
    scroll_delay = 1

    # Loop to perform scrolling
    for _ in range(scroll_count):
        # Execute JavaScript to scroll to the bottom of the page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Pause for a moment to allow the content to load
        time.sleep(scroll_delay)

    # Parse the HTML
    html = browser.html

    # Create a BeautifulSoup object from the scraped HTML
    market_soup = soup(html, 'html.parser')
    # Check if HTML was scraped correctly

    browser.quit()

    # Extract all the necessary info and insert into lists
    titles_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
    titles_list = [title.text.strip() for title in titles_div]
    prices_div = market_soup.find_all('span',
                                      class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
    prices_list = [price.text.strip() for price in prices_div]
    mileage_div = market_soup.find_all('span',
                                       class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1nxh6w3 x1sibtaa xo1l8bm xi81zsa")
    mileage_list = [mileage.text.strip() for mileage in mileage_div]
    #x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv
    #x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv
    urls_div = market_soup.find_all('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")
    urls_list = [url.get('href') for url in urls_div]

    print("Numbers of  vehicules found " + str(len(urls_div)))
    # Create a regular expression pattern to match city and state entries like "City, State"
    pattern = re.compile(r'(\w+(?:-\w+)?, [A-Z]{2})')

    # Initialize an empty list to store adjusted mileage entries
    mileage_list2 = []

    # Iterate through the original mileage entries
    for item in mileage_list:
        # Append the current mileage entry to the adjusted list
        mileage_list2.append(item)

        # Check if the current mileage entry matches the pattern and there are at least two entries in the adjusted list
        if pattern.match(item) and len(mileage_list2) >= 2 and pattern.match(mileage_list2[-2]):
            # If the conditions are met, insert "0K km" in between the two consecutive city and state entries
            mileage_list2.insert(-1, '0K km')

    # Extracted mileage list (separate from location and extract numeric values only)
    # Define regular expressions to extract numeric mileage values in "K km" and "K miles" format
    mileage_pattern = r'(\d+) km'
    mileage_pattern_km = r'(\d+)K km'
    mileage_pattern_miles = r'(\d+)K miles'

    # Initialize an empty list to store cleaned mileage values
    mileage_clean = []

    # Iterate through the adjusted mileage entries
    for item in mileage_list2:
        # Try to find a match for the "K km" format
        match_mileage_km = re.search(mileage_pattern_km, item)
        match_mileage = re.search(mileage_pattern, item)
        # Try to find a match for the "K miles" format
        match_mileage_miles = re.search(mileage_pattern_miles, item)

        # Check if either of the formats is found
        if  match_mileage or match_mileage_km or match_mileage_miles:
            # If "K km" format is found, convert it to meters and append to the cleaned list
            if match_mileage_km:
                mileage_clean.append(int(match_mileage_km.group(1)) * 1000)
            # If "K miles" format is found, convert it to meters and append to the cleaned list
            elif match_mileage_miles:
                mileage_clean.append(int(match_mileage_miles.group(1)) * 1600)
            elif match_mileage:  # km with no "K"
                mileage_clean.append(int(match_mileage.group(1)))

    # add all values to a list of dictionaries
    vehicles_list = []

    for i, item in enumerate(titles_list):
        cars_dict = {}

        if make.lower() not in titles_list[i].lower() and model.lower() not in titles_list[i].lower():
            print(f'droping result "{item}" https://www.facebook.com/{urls_list[i]}.')
            continue

        title_split = titles_list[i].split()

        cars_dict["Year"] = int(title_split[0])
        cars_dict["Make"] = title_split[1]
        cars_dict["Model"] = title_split[2] if len(title_split) > 2 else title_split[1]


        # Try to parse price string, if fails use default val '0'.
        price = '0' 
        try:
            price_digits = re.sub(r'[^\d.]', '', prices_list[i])
            price = int(price_digits)
        except ValueError: pass  # Do nothing
        cars_dict["Price"] = price

        cars_dict["Mileage"] = mileage_clean[i]
        cars_dict["URL"] = urls_list[i]
        vehicles_list.append(cars_dict)

    #print(vehicles_list)

    print(f'Final vehicles count: {len(vehicles_list)}')
    vehicles_df = pd.DataFrame(vehicles_list)

    # add prefix to the URL's
    vehicles_df['URL'] = 'https://www.facebook.com/' + vehicles_df['URL']

    # Filter the DataFrame to include rows where the 'Model' column matches the specified model, regardless of case.
    #filtered_df = vehicles_df[vehicles_df['Model'].str.lower() == model.lower()]
    vehicles_df.to_csv("carros.csv", encoding='utf-8')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrap()
