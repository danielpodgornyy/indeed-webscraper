from bs4 import BeautifulSoup
from selenium import webdriver
import time

def GetJobInfo(pgNum, inputLink):
    browser = webdriver.Chrome()
    browser.get(inputLink)
    soup = BeautifulSoup(browser.page_source,"lxml")

    browser.close()

    jobOpenings = soup.find_all("div",class_ = "cardOutline")
    
    for jobOpening in jobOpenings:
        jobTitle = jobOpening.find(class_ = "jobTitle").text
        companyName = jobOpening.find("span", class_ = "css-1x7z1ps").text
        location = jobOpening.find("div", class_ = "css-t4u72d").text
        extraInfo = jobOpening.find(class_="css-1ihavw2")
        link = "www.indeed.com" + jobOpening.find("a")["href"]


        print(jobTitle)
        print(companyName)
        print(location)
        if extraInfo is not None:
            print(extraInfo.text)
        else:
            print("None")
        print(link)
        print("")

    nextPage = pgNum + 1
    nextLink = "https://www.indeed.com" + soup.find(attrs = {"aria-label" : nextPage})["href"]
    print(nextLink)
    return nextLink

    
    
    
    
if (__name__ == "__main__"):
    nextLink = "https://www.indeed.com/jobs?q=software+engineer+intern&l=Dallas%2C+TX&radius=50&vjk=d3bb61d716c96bac"
    for pgNum in range(1,4):
        nextLink = GetJobInfo(pgNum, nextLink)


