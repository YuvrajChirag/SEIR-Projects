import sys
import requests
from bs4 import BeautifulSoup

def show_data(url):
    try:
        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    except:
        print("URL not working")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Title.
    print("\nTITLE:\n")

    if soup.title:
        print(soup.title.get_text().strip())
    else:
        print("No title found")

    print("\n")

    # Body.
    print("BODY:\n")

    # remove script and style.
    for i in soup(["script","style"]):
        i.decompose()

    body = soup.get_text()
    lines = body.split("\n")

    for j in lines:
        j = j.strip()
        if j != "":
            print(j)

    print("\n")

    # All Links.
    print("ALL LINKS:\n")
    for each_link in soup.find_all("a"):
        href = each_link.get("href")
        if href:
            print(href)

# main
if len(sys.argv) != 2: # wrong url or input.
    sys.exit()

url = sys.argv[1]
show_data(url)