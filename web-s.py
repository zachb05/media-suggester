from bs4 import BeautifulSoup
import requests
import csv

def contains_keyword(keywords, review):
    for keyword in keywords:
        if not keyword.lower() in get_review_text(review).lower():
            return False
    return True

def get_review_text(review):
    return review.find("div", attrs={"class":"text"}).text

titles = list()
reviews = list()
ratings = list()
links = list()

keywords = input("What keyword do you want to search for? (For multiple terms, separate with a comma and space) ").split(", ")
    
iteration = 0
while len(reviews) < 10:
    iteration += 1
    print(iteration)
    page_to_scrape = requests.get("https://myanimelist.net/reviews.php&p={iteration}")
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    review_list = soup.findAll("div", attrs={"class":"review-element"})
    
    for review in review_list:
        if not contains_keyword(keywords,review):
            continue
        
        raw_review = get_review_text(review)
        reviews.append(raw_review.strip().replace("...", "").replace("\n", "").replace("\r", "").replace("\t", ""))
        
        title = review.find("a", attrs={"class":"title"})
        titles.append(title.text)
        
        link = title['href']
        links.append(link)
        
        page_to_scrape = requests.get(link)
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        rating = soup.find("div", attrs={"class":"score-label"}).text
        ratings.append(rating)
        
        if len(reviews) >= 10:
            break
    
file = open("suggested_media.csv", "w")
writer = csv.writer(file)

writer.writerow(["Titles", "Reviews", "Ratings", "Links"])
                 
for title, review, rating, link in zip(titles, reviews, ratings, links):
    writer.writerow([title, review, rating, link])
file.close()