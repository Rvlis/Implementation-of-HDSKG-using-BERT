"""
spider contents from url：https://stackoverflow.com/tags/****/info

"""
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def data_spider():
    """
    :return contents: list, every item is the content of webpage
    """
    contents = list()
    with open("../txts/tags.txt", "r") as f:
        tags = f.readlines()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
        # print(tags)
        print("----------Spider data process----------")
        for tag in tqdm(tags):
            tag = tag.strip("\n")
            if tag != "":

                url = "https://stackoverflow.com/tags/" + tag + "/info"
                req = requests.get(url, headers=headers)
                soup = BeautifulSoup(req.text, "lxml")

                try:
                    p_tags = soup.find("div", attrs={"class":"s-prose js-post-body"}).find_all("p")
                except:
                    continue

                content = ""
                for item in p_tags:
                    item_content = item.get_text().strip()
                    if(len(item_content) <= 40 or item_content.find("?") != -1):
                        continue
                    # item_content = item_content.replace("It ",tag+" ").replace(" it "," "+tag+" ")
                    content = content + " " + item_content
                
                # print(content)
                contents.append(content)
    # print(contents)
    return contents


