from bs4 import BeautifulSoup
import requests
import csv

# Checks if keywords are in the text retrieved by a single page of reviews
def contains_keyword(keywords, review):
    for keyword in keywords:
        if not keyword.lower() in get_review_text(review).lower():
            return False
    return True

# Returns the review text within the soup instance 'review'
def get_review_text(review):
    return review.find("div", attrs={"class":"text"}).text

# Checks if review has already been tracked
def is_same_review(title, titles):
    for text in titles:
        if text == title:
            return True
    return False

# Lists to hold .csv entries
titles = list()
reviews = list()
ratings = list()
links = list()

keywords = input("What keyword do you want to search for? (For multiple terms, separate with a comma and space) ").split(", ")
    
iteration = 0
while len(reviews) < 10:
    iteration += 1
    print("Searching page " + str(iteration) + "...")
    
    # Sifts through MAL's 'New reviews' page
    page_to_scrape = requests.get("https://myanimelist.net/reviews.php&p={iteration}")
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    review_list = soup.findAll("div", attrs={"class":"review-element"})
    
    # Appends information to above lists iff keywords are contained in review text
    for review in review_list:
        if not contains_keyword(keywords,review):
            continue
        
        title = review.find("a", attrs={"class":"title"})
        if is_same_review(title.text, titles):
            continue
        titles.append(title.text)
        
        raw_review = get_review_text(review)
        reviews.append(raw_review.strip().replace("...", "").replace("\n", "").replace("\r", "").replace("\t", ""))
        
        link = title['href']
        links.append(link)
        
        page_to_scrape = requests.get(link)
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        rating = soup.find("div", attrs={"class":"score-label"}).text
        ratings.append(rating)
        
        # Ceases search after 10 valid reviews have been found
        if len(reviews) >= 10:
            break
    
    # Ceases search after 50 pages (250 reviews)
    if iteration >= 50:
        print("Not enough reviews (" + str(len(titles)) + ") found with keywords " + str(keywords[:]))
        break
    
# Writes to a .csv file if at least 1 review was found
if len(titles) > 0:
    file = open("suggested_media.csv", "w")
    writer = csv.writer(file)

    writer.writerow(["Titles", "Reviews", "Ratings", "Links"])
                    
    for title, review, rating, link in zip(titles, reviews, ratings, links):
        writer.writerow([title, review, rating, link])
    file.close()