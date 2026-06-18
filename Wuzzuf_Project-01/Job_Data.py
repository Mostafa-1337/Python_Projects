#import libraries
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

#list for lxml
job_title = []
company_name = []
location_name = []
links = []
time = []


#request url
result = requests.get("https://wuzzuf.net/search/jobs?q=python&a=hpb%7Cspbg")
src = result.content

#soup
soup = BeautifulSoup(src,"lxml")
job_titles = soup.find_all("h2",{"class":"css-193uk2c"})
company_names = soup.find_all("a",{"class":"css-ipsyv7"})
location_names = soup.find_all("span",{"class":"css-16x61xq"})
_time = soup.find_all("a",{"class":"css-a85cz4"})



#Loops
for i in range(len(job_titles)):
    job_title.append(job_titles[i].text)
    company_name.append(company_names[i].text)
    location_name.append(location_names[i].text)
    links_path = job_titles[i].find("a").attrs['href']
    links.append(f"https://wuzzuf.net{links_path}")
    time.append(_time[i].text)


#Write as file with csv
file_list = [job_title, company_name, location_name, links, time]
unp = zip_longest(*file_list)
with open("job_data.csv","w") as file:
    wr = csv.writer(file)
    wr.writerow(["Title", "Company", "Location", "Links", "Time"])
    wr.writerows(unp)
print("Done!")
print("Check The File")