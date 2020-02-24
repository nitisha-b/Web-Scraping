# Written By: Nitisha Bhandari
# This program pulls out all the API names, their URL, their categories, and their 
# descriptions from ProgrammableWeb's API Directory, and exports it as a csv file. 
# This uses Beautiful Soup, requests, and pandas library.

from bs4 import BeautifulSoup
import requests 
import pandas as pd

url = "https://www.programmableweb.com/category/all/apis"
#url = "https://www.programmableweb.com/category/all/apis?page=2000"

api_no = 0
api_dict = {}
page = 1

while(True):

	response = requests.get(url)
	data = response.text 
	soup = BeautifulSoup(data, 'html.parser')

	# apis = soup.find_all("table", {"class":"views-table cols-4 table"})
	apis = soup.find_all("tr", {"class":["odd", "even"]})
	# print(apis)

	for api in apis:
		name_tag = api.find("td", {"class" : "views-field views-field-pw-version-title"})
		name = name_tag.text
		link_rel = name_tag.find("a").get("href")
		link_abs = "https://www.programmableweb.com" + link_rel
		description = api.find("td", {"class" : "views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8"}).text
		category_tag = api.find("td", {"class" : "views-field views-field-field-article-primary-category"})
		# category = category_tag.find("a").text if category_tag else "N/A"
		
		if(category_tag.find("a")):
			category = category_tag.find("a").text
		else:
			category = "N/A"

		#print("name:", name, "cat: ", category)

		api_no += 1
		api_dict[api_no] = [name, link_abs, category, description]

		#print("Name: ", name, "\nURL: ", link_abs, "\nDescription: ", description, "\nCategory: ", category, "\n--------------------")

	url_tag = soup.find("a", {"title" : "Go to next page"})

	#print(url_tag.get("href"))

	if(url_tag):
		page += 1
		url = "https://www.programmableweb.com" + url_tag.get("href")
		#print(url)
	else:
		break

print("Pg: ", page)
print("Total APIs: ", api_no)
#print(api_dict)

api_df = pd.DataFrame.from_dict(api_dict, orient="index", columns = ["Name", "Link", "Category", "Description"])

api_df.to_csv('apis.csv')

