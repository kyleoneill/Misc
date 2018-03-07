import requests
import sys
from bs4 import BeautifulSoup
from prettytable import PrettyTable

def getWeather(soup):
    locationID = soup.find(id="seven-day-forecast")
    location = (locationID.find('h2')).get_text()

    currentTempID = soup.find(id="current-conditions-body")
    currentTemp = (currentTempID.find(class_="myforecast-current-lrg")).get_text()
    
    sevenDay = soup.find(id="seven-day-forecast")
    forecastItems = sevenDay.find_all(class_="tombstone-container")

    print(location)
    table = PrettyTable(['Day','Description', 'Temp'])
    table.add_row(["Now", forecastItems[0].find(class_="short-desc").get_text(), currentTemp])
    table.add_row(["","",""])
    for day in forecastItems:
        try:
            period = day.find(class_="period-name").get_text()
            desc = day.find(class_="short-desc").get_text()
            temp = day.find(class_="temp").get_text()
        except AttributeError:
            continue
        table.add_row([period, desc, temp])
        table.add_row(["","",""])
    print(table)

def getLocation(address):#Gets the url for a city using an input address
    page = requests.get("http://www.weather.gov")
    soup = BeautifulSoup(page.content, 'html.parser')
    action = soup.find('form', id='getForecast').get('action')#Find address input form
    newurl = action + "?inputstring=" + str(address)#Link to an address' weather page
    return newurl

def verifyAddress(url):#Verifies that an address returns a page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if str(soup.find('title')) == "<title>City State &amp; Zipcode Search Page</title>":#If address did not work
        state = input("Enter state abbreviation (NY, PA, etc.): ")#Assume that there is more than one town of this name in the US, enter state to narrow down search
        cityList = soup.find_all('a')#Gets a list of all links to towns with input name
        refList = []
        for reference in cityList:#Check each link and compare it to the input state
            if " " + state + " " in reference.get_text():
                refList.append(reference)
        if len(refList) == 1:#If only one town exists in a state, use its link
            link = reference['href']
        elif len(refList) > 1:#If a state has more than one town with the input name, enter the county to further narrow down the search
            county = input("Enter the county name: ")
            for ref in refList:
                if county in ref.get_text():
                    link = ref['href']
                    break
        try:
            page = requests.get(link)#open a page with the created link and try to return the soup object
            soup = BeautifulSoup(page.content, 'html.parser')
        except UnboundLocalError:
            print("Invalid state/county.")#If there was an error, print that an input was incorrect
            sys.exit()
    return soup

def main():
    if len(sys.argv) == 2: #If only one argument is entered (zip code, short town) that is the address
        address = sys.argv[1]
    elif len(sys.argv) > 2:#If more than one arg is entered, the address string is concatenated
        address = ' '.join(sys.argv[1:])
    else:#If no args are entered, the user is prompted to enter an address or zip
        address = input("Input town/city or postal code: ")
    locationLink = getLocation(address)
    soupObj = verifyAddress(locationLink)
    getWeather(soupObj)

main()