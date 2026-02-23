import requests
from bs4 import BeautifulSoup
import re

def compare_sites(): #Function to compare two websites using Simhash.

    print("---- WEBSITE SIMILARITY CHECKER ----\n")

    while True: # take first url
        siteA = input("Enter first website URL: ").strip()
        if siteA.startswith("http://") or siteA.startswith("https://"):
            break
        else:
            print("Enter valid URL starting with http/https")

    while True: # take second url
        siteB = input("Enter second website URL: ").strip()
        if siteB.startswith("http://") or siteB.startswith("https://"):
            break
        else:
            print("Enter valid URL starting with http/https")

    print("\nLoading websites...\n")

    def extract_text(link): # function to extract clean text.
        try:
            head = {"User-Agent": "Mozilla/5.0"}
            page = requests.get(link, headers=head, timeout=10)

            soup = BeautifulSoup(page.text, "html.parser")

            for noise in soup(["script","style","nav","header","footer"]): # remove unwanted tags
                noise.decompose()

            data = soup.get_text(separator=" ")
            return data.lower()

        except:
            print("Cannot open:", link)
            return ""

    textA = extract_text(siteA)
    textB = extract_text(siteB)

    def make_dict(txt): # word counter.
        tokens = re.findall(r"[a-zA-Z0-9]+", txt)
        store = {}
        for t in tokens:
            store[t] = store.get(t,0) + 1
        return store

    dictA = make_dict(textA)
    dictB = make_dict(textB)

    # polynomial hash constants.
    base = 37
    mod = 2**64

    def build_hash(word): # word hash function.
        val = 0
        mul = 1
        for ch in word:
            val = (val + ord(ch)*mul) % mod
            mul = (mul*base) % mod
        return val

    def build_simhash(d): # simhash generator.
        bucket = [0]*64

        for word,count in d.items():
            hv = build_hash(word)

            for i in range(64):
                if (hv>>i)&1:
                    bucket[i] += count
                else:
                    bucket[i] -= count

        final = 0
        for i in range(64):
            if bucket[i] > 0:
                final = final | (1<<i)

        return final

    signA = build_simhash(dictA)
    signB = build_simhash(dictB)

    print("Signature 1:", signA)
    print("Signature 2:", signB)

    match = 0 # common bits.
    for i in range(64):
        if ((signA>>i)&1) == ((signB>>i)&1):
            match += 1

    print("\nMatching bits:", match, "/ 64")
    print("Similarity:", round(match/64*100,2), "%")

compare_sites() # call function