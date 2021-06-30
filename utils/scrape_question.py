import requests
from bs4 import BeautifulSoup

def get_data_from_url(id: int, url: str):
    
    data = {}
    page = requests.get(url)
    if page.status_code != 200:
        data['status'] = "failure"
        data['content'] = None
        return data
    soup = BeautifulSoup(page.content, features="html5lib")
    
    problem = soup.find('div', attrs = {'class':'problem-statement'})
    if problem is None:
        data['status'] = "failure"
        data['content'] = None
        return data
    intro = soup.find('div', attrs = {'class':'row problem-intro__row'})
    intro_heading = intro.find('span', attrs={'class':'problem-tab__name'})
    metadata = soup.find('div', attrs = {'class':'row problem-meta-summary'})
    level = metadata.find('strong', attrs={'class':'problem-tab__problem-level'})
    
    accuracy_snippet = metadata.find("span", attrs={"class":"problem-tab__problem-accuracy"})
    accuracy = accuracy_snippet.find("span", attrs={"class":"problem-tab__value"})
    accuracy = float(accuracy.text.strip()[:-1])
    
    with open("../temp/" + str(id) + ".txt", "w+") as f:
        for line in problem.text:
            f.write(line)
    
    data = {}
    data["status"] = "success"
    data["intro"] = intro_heading.text.strip()
    data["level"] = level.text.strip()
    data["accuracy"] = accuracy
    data["intro"] = data["intro"].replace("'", "")
    data["intro"] = data["intro"].replace('"', '')
    return data

# get_data_from_url(0, "https://practice.geeksforgeeks.org/problems/find-optimum-operation4504/0")
print(get_data_from_url(142, "https://practice.geeksforgeeks.org/problems/-minimum-number-of-coins/0#"))