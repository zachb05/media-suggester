# media-suggester

This is a web scraping project that writes to a .csv file.

## Description
Using Python and the BeautifulSoup4 library, Media Suggester scrapes various MyAnimeList.net webpages for anime recommendations. 

I chose BeautifulSoup for ease of use. However, I found it difficult to make this project into a website using PyScript. The Requests library is unsupported. I am open to any contributions.

## Installation
Download Python3 and pip install bs4 to properly run the project in your chosen developer environment.

## Usage
Upon running the code, you will be prompted at the terminal to place a keyword, or multiple keywords separated by a comma (e.g. Beautiful, Charming), to narrow down the search. Beautiful Soup will begin sifting through MAL's new reviews page to find 10 reviews that match **all** keywords placed. Once found, suggested_media.csv will be written locally with the 10 animes and their respective titles, reviews, rating, and link. If 10 reviews cannot be found within the first 50 pages, the program will stop and write only however many it has found up until that point to the .csv file (if it is none, a .csv file will not be made). 