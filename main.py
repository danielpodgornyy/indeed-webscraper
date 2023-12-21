from openpyxl import Workbook

def checkWorkbookExists():
    from os import path
    from openpyxl import load_workbook

    if path.exists("./JobListings.xlsx"):
        currWB = load_workbook(filename = "JobListings.xlsx")
    else:
        currWB = Workbook()
        currWB['Sheet'].title = "Indeed_Listings"

    return currWB


def ImportJobInfo(currPg, inputLink, WB, currRowPos, newWidthDimensions):
    from bs4 import BeautifulSoup
    from selenium import webdriver

    browser = webdriver.Chrome()
    browser.get(inputLink)
    soup = BeautifulSoup(browser.page_source,"lxml")

    browser.close()

    jobOpenings = soup.find_all("div",class_ = "cardOutline")
    
    FirstSheet = WB["Indeed_Listings"]
    itemLetters = ["A", "B", "C", "D", "E"]

    widthDimensions = newWidthDimensions
    for counter, jobOpening in enumerate(jobOpenings, start = currRowPos):

        jobTitle = jobOpening.find(class_ = "jobTitle").text
        companyName = jobOpening.find("span", class_ = "css-1x7z1ps").text
        location = jobOpening.find("div", class_ = "css-t4u72d").text
        extraInfo = jobOpening.find(class_="css-1ihavw2")
        link = "www.indeed.com" + jobOpening.find("a")["href"]

        itemAttr = [companyName, jobTitle, location, extraInfo, link]

        for letter,attribute in zip(itemLetters, itemAttr):
            if (attribute is not None):
                if (letter == "D"):
                    FirstSheet[letter + str(counter)] = attribute.text
                    continue

                FirstSheet[letter + str(counter)] = attribute
                widthDimensions[letter] = max(widthDimensions[letter], len(attribute))
    
    
    for letter in itemLetters:
        FirstSheet.column_dimensions[letter].width = widthDimensions[letter]
        


    currRowPos = currRowPos + len(list(jobOpenings))
    nextPage = currPg + 1
    nextLink = "https://www.indeed.com" + soup.find(attrs = {"aria-label" : nextPage})["href"]
    #print(nextLink)
    return nextLink, currRowPos, widthDimensions

if (__name__ == "__main__"):
    wb = checkWorkbookExists()
    nextLink = "https://www.indeed.com/jobs?q=software+engineer+intern&l=Dallas%2C+TX&radius=50&vjk=d3bb61d716c96bac"
    rowPos = 1
    inputWidthDims = {"A" : 0, "B" : 0, "C" : 0, "D" : 0, "E" : 0}

    for pgNum in range(1,4):
        nextLink, rowPos, inputWidthDims = ImportJobInfo(pgNum, nextLink, wb, rowPos, inputWidthDims)

        
    wb.save(filename = "JobListings.xlsx")


