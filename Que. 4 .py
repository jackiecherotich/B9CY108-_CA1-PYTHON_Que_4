# Web scraping to CSV
# The  two hotel booking sites have the same HTML structure

from bs4 import BeautifulSoup
import requests
import csv
import os

# ----------------------------------------------------
CSV_FILE = "Combined_Hotel_Rooms_Details.csv"

#----------------------------------------------------
def main():
    url_1 = "https://hotel1.tiiny.site/"
    url_2 = "https://booking-hotels2.tiiny.site/"

    web_scraping_hotels(url_1)
    web_scraping_hotels(url_2)

    display_csv_raw()



# -------------Web Scrapping function----------------------
def web_scraping_hotels(url):
    print(f"Scraping {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())
    cards = soup.find_all("div", class_="hotel-card")

    file_exists = os.path.exists(CSV_FILE)

# Opening csv file
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        #  Headings 
        if not file_exists:
            writer.writerow([
                "Name",
                "Location",
                "Distance from downtown",
                "Description",
                "Current price (€)",
                "More information",
                "Website"
            ])

        # --------Extracting from the html structure-------------------
    
        for card in cards:
            try:
                # hotel info section
                card_info = card.find("div", class_="hotel-info")

                name = card_info.find("div", class_="hotel-name").text
                location = card_info.find("div", class_="hotel-location").text
                distance_from_downtown = card_info.find(
                    "div", class_="hotel-distance"
                ).get_text(strip=True).replace("from downtown", "")
                description = card_info.find(
                    "div", class_="hotel-description"
                ).get_text(strip=True)

                # price section
                prices_section = card.find("div", class_="hotel-pricing")

                # rating 
                rating = prices_section.find(
                    "div", class_="rating-score"
                ).text

                # price
                current_price = prices_section.find(
                    "div", class_="current-price"
                ).text
                #current_price = float(current_price)

                # nights info
                more_information = prices_section.find(
                    "div", class_="nights-info"
                ).text

                # ---------Writing to csv------------------------------
                writer.writerow([
                    name,
                    location,
                    distance_from_downtown,
                    description,
                    current_price,
                    more_information,
                    url
                ])

            except Exception as e:
                print("Error processing a hotel card:", e)
                continue


# ------------Displaying csv----------------------------------------
def display_csv_raw():
    print("\n--- Displaying csv file ---\n")
    with open(CSV_FILE, "r") as f:
        print(f.read())


# ----------------------------------------------------
if __name__ == "__main__":
    main()
