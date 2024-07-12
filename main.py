import requests
from bs4 import BeautifulSoup
import json
import time
from job_agent import run_analysis
import sys

def scrape_job_descriptions(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div with class 'mt4'
        div_content = soup.find_all('div', class_='show-more-less-html__markup')

        # Extract and return the inner HTML of each found div
        return [div.prettify() for div in div_content]
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []


keyword = sys.argv[1]
location = sys.argv[2]
llm_model = sys.argv[3]

# LinkedIn job search full
full_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={location}&f_E=4&f_WT=3%2C1"  # pass 24h, hybrid or onsite, mid senior


# LinkedIn job search URL basic 
url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location={location}&f_WT=3%2C1&f_E=4&start=1"  # pass 24h

# Make a GET request to fetch the webpage
response = requests.get(full_url)
webpage = response.content


# Parse the HTML content
soup = BeautifulSoup(webpage, 'html.parser')

# Get total job for iteration
total_job = int(soup.find('span', class_='results-context-header__job-count').text.strip())

print(f"total job: {total_job}")

response = requests.get(url)
webpage = response.content

# Parse the HTML content
soup = BeautifulSoup(webpage, 'html.parser')

# Find all job posting elements
job_postings = soup.find_all('div', class_='job-search-card')


# List to store job details
jobs_list = []

job_count = 0

with open(f"{keyword}_{location}_{llm_model}", "w") as w:
    while job_count < total_job:
        # Extract details from each job posting
        for job in job_postings:
            title = job.find('h3', class_='base-search-card__title').text.strip()
            location = job.find('span', class_='job-search-card__location').text.strip()
            company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_link = job.find('a', class_='base-card__full-link')['href']
            
            # Add the job details to the list

            job_description = scrape_job_descriptions(job_link)
            print(title)
            print(job_link)
            print(location)
            w.write(f"Title: {title}\nLink: {job_link}\nLocation: {location}\n")
            # print(job_description)
            message = run_analysis(job_description, llm_model)
            jobs_list.append({
                'title': title,
                'company': company,
                'location': location,
                'link': job_link,
                'verdict': message["result"]
            })
            #print(message["result"])
            w.write(message["result"])
            #print("============================")
            w.write("\n============================\n")
            #print()
            job_count = job_count + 1
            # if job_count == 10:
            #     break
            time.sleep(1)
        if job_count >= total_job:
            break
        else:
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location={location}&f_WT=3%2C1&f_E=4&start={job_count}"  # pass 24h

            # Make a GET request to fetch the webpage
            response = requests.get(full_url)
            webpage = response.content
            soup = BeautifulSoup(webpage, 'html.parser')

            # Find all job posting elements
            job_postings = soup.find_all('div', class_='job-search-card')





# print(jobs_list)

# Output the job details to a JSON file
timestamp = time.time()
with open(f"{timestamp}_linkedin_jobs.json", 'w') as outfile:
    json.dump(jobs_list, outfile, indent=4)
