import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL=f'https://www.indeed.com/jobs?q=physics&limit={LIMIT}'

def extract_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text,'html.parser')
  pagination = soup.find('div',{'class':'pagination'})
  links = pagination.find_all('a')
  pages=[]
  for link in links[0:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_jobs(html):  
  title = html.find('h2',{'class':'title'}).find('a')['title']
  company = html.find('span',{'class':'company'})
  company_a = company.find('a')
  if company_a is None:
   company = str(company.string)
  else:
   company = str(company_a.string)
  company = company.strip()
  location = html.find('div',{'class':'recJobLoc'})['data-rc-loc']
  job_id = html['data-jk']
  return{'title': title, 'company': company, 'location' : location, 'link' : f'https://www.indeed.com/viewjob?jk={job_id}'}
  

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f'{URL}&start={page*LIMIT}')
    soup = BeautifulSoup(result.text,'html.parser')
    results = soup.find_all('div',{'class':'jobsearch-SerpJobCard'})
    for result in results:
      job = extract_jobs(result)
      jobs.append(job)
  return jobs
  
def get_jobs():
  jobs = extract_indeed_jobs(extract_last_page(URL))
  return jobs