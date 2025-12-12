# Web scrapping to csv
# The two sites had same html structure

from bs4 import BeautifulSoup
import requests
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 2000)
import os

#-------------------------------------------------------------------#
#-------------------WEB SCRAPING FUNCTION----------------------------#
# function to scrape data since the 2 hotels have same html structure
def web_scraping_hotels(url):
    print(f"Scraping {url}")
    results = []
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Could not load {url}")
        return results

    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    cards = soup.find_all("div", class_="hotel-card")

    # Hotel details
    for card in cards:
        try:

            # hotel info section
            card_info = card.find("div", class_="hotel-info")

            name = card_info.find("div", class_="hotel-name").text
            location = card_info.find("div", class_="hotel-location").text
            distance_from_downtown = card_info.find("div", class_="hotel-distance").get_text(strip=True).replace("from downtown", "")
            description = card_info.find("div", class_="hotel-description").get_text(strip=True)

            # price section
            prices_section = card.find("div", class_="hotel-pricing")

            # rating
            rating = prices_section.find("div", class_="rating-score").text

            # price
            current_price = prices_section.find("div", class_="current-price").text
            current_price= float(current_price[2:])

            # nights info
            more_information = prices_section.find("div", class_="nights-info").text


        # referencing

            results.append({
                'Name': name,
                'Location': location,
                'Distance from downtown': distance_from_downtown,
                'Description': description,
                'Current price (€)': current_price,
                'More information': more_information,
                "Website": url

            })
        except Exception as e:
           print(f" Error checking a card: {e}")
           continue

    return results

#---------------------------------------------------------------------------------#
#---------------------SAVE DETAILS TO CSV-----------------------------------------#
def save_to_csv(df,csv_filename):
    try:
        if not os.path.exists(csv_filename):
            df.to_csv(csv_filename, index=False)
            print("\nCSV file created successfully:", csv_filename)

        else:
            df.to_csv(csv_filename,mode ='a',index=False,header=False)
            print(f"{csv_filename} already exists.Data appended")
    except Exception as e:
        print(f" Error saving CSV file: {e}")
#---------------------------------------------------------------------------------#
#------------------------READING AND DISPLAYING CSV-------------------------------#

def display_from_csv(csv_filename):
    try:
        print("\n----- Reading data from csv file -----\n")
        df_read = pd.read_csv(csv_filename)
        print(df_read)
        input("\nPress any key to continue...")
    except Exception as e:
        print(f" Error reading data from CSV file: {e}")


#----------------------------------------------------------------------------#
#-------------------------MAIN FUNCTION--------------------------------------#
def main():
    url_2 = "https://booking-hotels2.tiiny.site/"
    url_1 = "https://hotel1.tiiny.site/"

    # print(soup_1.prettify())
    # print(soup_2.prettify())
   # Calling web scrapping function for the 2 website
    hotel1_details = web_scraping_hotels(url_1)
    hotel2_details = web_scraping_hotels(url_2)


    # Combining data and converting to data frames
    hotel1_details.extend(hotel2_details)
    df = pd.DataFrame(hotel1_details)

 # calling the save function to save
    filename = "Hotel_Rooms_Comparison.csv"
    save_to_csv(df, filename)

    # Calling Display results function
    display_from_csv(filename)

#-------------------------------------------------------------------------------#
#-----------------BEGINNING OF EXECUTION----------------------------------------#
if __name__ == "__main__":
    main()






