from bs4 import BeautifulSoup
import csv
import requests

page_to_scrape = requests.get("https://myanimelist.net/anime/season")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

titles = soup.findAll("a", href = True, attrs={"class":"link-title"})
ratings = soup.findAll("div", attrs={"title":"Score"})

file = open("scraped_animes.csv", "w")
writer = csv.writer(file)

writer.writerow(["Titles", "Ratings"])
                 
for title, rating in zip(titles, ratings):
    if "N/A" in rating.text:
        continue
    if float(rating.text) >= 8:
        writer.writerow([title.text, rating.text])
file.close()