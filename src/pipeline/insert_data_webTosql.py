import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
import pyodbc

def get_jobDescription(link):
    url = 'https://www.reed.co.uk' + link
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    description = soup.find('span', itemprop='description')
    return description.text.strip() if description else 'nodata'

def get_jobData(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    data = soup.find_all('header')
    job_title, job_descriptions, salary = [], [], []
    
    for i in data:
        if not (i.h2 and i.ul):
            continue
        job_title.append(i.h2.text)
        job_descriptions.append(get_jobDescription(i.h2.a['href']))
        salary.append(i.ul.li.text)

    return pd.DataFrame({
        'job_title': job_title,
        'job_description': job_descriptions
    })

def get_all_page_data(url, maxpage):
    dfs = [get_jobData(requests.get(url + str(i)).text) for i in range(1, maxpage + 1)]
    time.sleep(1)
    return pd.concat(dfs, ignore_index=True)

data = get_all_page_data('https://www.reed.co.uk/jobs/data-scientist-jobs-in-united-kingdom?agency=true&direct=true&pageno=', 10)

# Connect to the SQL Server database
conn_str = 'DRIVER={SQL Server};SERVER=HP-ELITEBOOK\SQLEXPRESS;DATABASE=job_scan;Trusted_Connection=yes;'
with pyodbc.connect(conn_str) as conn:
    with conn.cursor() as cursor:
        for _, row in data.iterrows():
            cursor.execute("""
            INSERT INTO job_data (job_title, job_description)
            VALUES (?, ?)
            """, row['job_title'], row['job_description'])