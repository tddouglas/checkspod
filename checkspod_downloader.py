import requests as r
import os
from bs4 import BeautifulSoup

# This is a script to iterate through all Checks & Balance episodes, pull the details page for the list overview,
# then query the details page to pull the associated .mp3 file from the only media request on the details page
# Should pull all files from January 17th, 2020 onward = 183 episodes. Episodes dynamic load so will need to solve
# How to get all episodes loaded on page to parse

'''
Results contain 0 - 182
JSON Schema Example:

info	
    page	1
    total	183
results	
    0	
        title	"Checks and Balance: Inequality qualities"
        alias	"checks-and-balance-inequality-qualities"
        show	"62e286a834d4d9a8af874246"
        owner	"609aac0a2f70a665d793b6fb"
        creationDate	"2023-07-14T17:46:24.681Z"
        publishDate	"2023-07-14T17:46:24.273Z"
        summary	'<p>By some measures,&nbsp;in the aftermath of the pandemic, income inequality in America is either increasing or remaining stubbornly high. On the left<strong>,</strong> the gap between rich and poor has long been an urgent issue<strong>—</strong>and more people on the right now agree. As both sides of the aisle look for solutions, they are reaching some <a href="https://www.economist.com/united-states/2023/07/13/the-american-left-and-right-loathe-each-other-and-agree-on-a-lot?utm_campaign=a.io&amp;utm_medium=audio.podcast.np&amp;utm_source=checksandbalance&amp;utm_content=discovery.content.anonymous.tr_shownotes_na-na_article&amp;utm_term=sa.listeners" rel="noopener noreferrer" target="_blank">surprisingly similar conclusions</a>. What are the proposed answers to economic inequality in America? How likely are they to be taken up?</p><p><br></p><p>Economist Thomas Piketty talks us through the state of economic inequality in America and some of the left’s proposals to reduce it. And Oren Cass of American Compass, a think tank, explains a new wave of conservative solutions to inequality.</p><p><br></p><p>John Prideaux hosts with Charlotte Howard and Idrees Kahloon.</p><p><br></p><p>You can now find every episode of Checks and Balance <a href="http://www.economist.com/checkspod" rel="noopener noreferrer" target="_blank">in one place</a> and sign up to our weekly <a href="https://www.economist.com/newsletters" rel="noopener noreferrer" target="_blank">newsletter</a>. For full access to print, digital and audio editions, as well as exclusive live events, subscribe to The Economist at<a href="http://economist.com/USpod" rel="noopener noreferrer" target="_blank"> economist.com/uspod</a>.&nbsp;</p>'
        type	"full"
        explicit	false
        audio	
        filename	"1689356564982-613ee4b82d0bf8720012488babe8e9e6.mp3"
        filetype	"audio/mpeg"
        originalname	""
        size	69742927
        url	"//s3.amazonaws.com/assets.pippa.io/shows/62e286a834d4d9a8af874246/1689356564982-613ee4b82d0bf8720012488babe8e9e6.mp3"
        duration	2905.683625
        status	"published"
        _id	"64b189f0e435a60011f67cf4"
        isStarter	false
'''
CHECKSPOD_EPISODES_JSON = "https://shows.acast.com/api/shows/57cc3c7d-b0fd-4930-9279-4e84c75df457/episodes?paginate=false&results=183"


def query_checkspod():
    episode_list_get = r.get(CHECKSPOD_EPISODES_JSON).json()
    for x, episode in enumerate(episode_list_get["results"]):
        # if x > 0:
        #     break

        filename = 'checkspod_files/' + episode["_id"] + '.mp3'
        if not os.path.isfile(filename):
            url = episode["audio"]["url"]
            querably_url = url.replace("//s3.amazonaws.com/", "")
            doc = r.get('https://' + querably_url)
            store_file(filename, doc.content)
        else:
            print("File already present")


def store_file(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)
