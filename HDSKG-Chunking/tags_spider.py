"""
spider tags 
url = "https://stackoverflow.com/tags?page=" + ### + "&tab=popular"
"""
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
import argparse

def tags_spider(start_index, end_index):
    """
    spider tags from pages[start_index, end_index]
    """
    print("-----------spider tag process----------")
    cnt = 0

    with open("../txts/tags.txt", "w") as wf:
         
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
        for num in tqdm(range(start_index, end_index+1)):

            url = "https://stackoverflow.com/tags?page=" + str(num) + "&tab=popular"
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            try:
                items = soup.find_all("a", attrs={"class":"post-tag"})
                cnt += len(items)
                for item in items:
                    # print(tag)
                    tag = item.get_text()
                    wf.write(tag+"\n")
            except:
                continue
        
        print("spider",cnt,"tags.")


# start_index = int(sys.argv[1])
# end_index = int(sys.argv[2])
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", type=int, default=1, help="start index of page")
    parser.add_argument("-e", "--end", type=int, default=5, help="end index of page")
    args = parser.parse_args()
    tags_spider(args.start, args.end)