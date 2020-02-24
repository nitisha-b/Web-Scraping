from bs4 import BeautifulSoup
import requests 
import pandas as pd

# Link of the webpage
url = "https://boston.craigslist.org/search/npo"
jobs_no = 0
npo_jobs = {}

while(True):
	# Get the webpage --> response value will be sth like 200, 400, 404
	response = requests.get(url)

	# Extract the source code of the page
	data = response.text

	# Pass the source code to beautiful soup to allow it to parse the text 
	soup = BeautifulSoup(data, 'html.parser')

	# Now, we can extract specific data from the page

	# Find all links or <a> tags 
	# tags = soup.find_all('a')

	# for tag in tags: 
	# 	print(tag.get('href'))

	# Find all a tags whose class name is "result-title"
	# titles = soup.find_all("a",{"class":"result-title"})

	# for title in titles:
	# 	print(title.text)

	# Find addresses 
	# addresses = soup.find_all("span", {"class": "result-hood"})

	# for address in addresses:
	# 	print(address.text)

	# Extract all the necessary information about the job wrapped in a <p> tag 
	jobs = soup.find_all("p", {"class":"result-info"})

	for job in jobs:
		title = job.find("a", {"class":"result-title"}).text
		location_tag = job.find("span", {"class": "result-hood"})
		location = location_tag.text[2:-1] if location_tag else "N/A"
		date = job.find("time", {"class":"result-date"}).text
		link = job.find("a", {"class":"result-title"}).get("href")

		job_response = requests.get(link)
		job_data = job_response.text
		job_soup = BeautifulSoup(job_data, 'html.parser')
		job_description = job_soup.find('section',{'id':'postingbody'}).text
		job_attributes_tag = job_soup.find('p',{'class':'attrgroup'})
		job_attributes = job_attributes_tag.text if job_attributes_tag else "N/A"
	    
		jobs_no+=1
		npo_jobs[jobs_no] = [title, location, date, link, job_attributes, job_description]

		#print('Job Title:', title, '\nLocation:', location, '\nDate:', date, '\nLink:', link,"\n", job_attributes, '\nJob Description:', job_description,'\n---------------')

	url_tag = soup.find("a", {"title": "next page"})
	if(url_tag.get("href")):
		url = "https://boston.craigslist.org" + url_tag.get("href")
		print(url)
	else:
		break

print("Total Jobs: ", jobs_no)
npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient='index', columns=["Job Title", "Job Location", "Date", "Link", "Job Attributes", "Job Description"])

#npo_jobs_df.head()
npo_jobs_df.to_csv('npo_jobs.csv')






# print(soup)