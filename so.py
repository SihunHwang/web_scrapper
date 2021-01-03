import requests
from bs4 import BeautifulSoup

URL =f'https://stackoverflow.com/jobs?q=physics'

def extract_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text,'html.parser')
  pagination = soup.find('div',{'class':'s-pagination'})
  links = pagination.find_all('span')
  last_page =links[-2].get_text(strip=True)
  return int(last_page)

def extract_jobs(html):
  title = html.find('h2',{'class':'mb4 fc-black-800 fs-body3'}).a['title']
  company = html.find('h3',{'class':'fc-black-700 fs-body1 mb4'}).find('span').get_text(strip=True)
  location = html.find('h3',{'class':'fc-black-700 fs-body1 mb4'}).find('span',{'class':'fc-black-500'}).get_text(strip=True)
  job_id = html['data-jobid']
  return {'title': title, 'company': company, 'location': location, 'link': f'https://stackoverflow.com/jobs/{job_id}/'}

def collect_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f'{URL}&pg={page+1}')
    soup = BeautifulSoup(result.text,'html.parser')
    results = soup.find_all('div',{'class':'-job'})
    for result in results:
      job = extract_jobs(result)
      jobs.append(job)
  return jobs
  




def get_jobs():
  last_page = extract_last_page()
  jobs = collect_jobs(last_page)
  return jobs

