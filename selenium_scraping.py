# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup
# import pandas as pd
# import time

# def configure_driver(driver_path):
#     service = Service(driver_path)
#     return webdriver.Chrome(service=service)

# def scrape_job_data(driver, start_page, end_page):
#     data = []
#     for i in range(start_page, end_page + 1):
#         url = f"https://www.naukri.com/python-developer-jobs-{i}?k=python%20developer"
#         driver.get(url)

#         # Wait for the job listings to load (you can adjust the sleep time as needed)
#         time.sleep(3)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         job_listings = soup.find_all('div', class_='srp-jobtuple-wrapper')

#         for job in job_listings:
#             title = job.find('a', class_='title').text
#             company = job.find('a', class_='comp-name').text
#             experience = job.find('span', class_='exp').text
#             salary = job.find('span', class_='sal').text
#             location = job.find('span', class_='loc').text
#             job_url = job.find('a', class_='title')['href']

#             try:
#                 skills = [tag.text for tag in job.find('ul', class_='tags-gt').find_all('li', class_='tag-li')]
#             except AttributeError:
#                 skills = []

#             data.append({
#                 'Title': title,
#                 'Company': company,
#                 'Experience': experience,
#                 'Salary': salary,
#                 'Location': location,
#                 'URL': job_url,
#                 'Skills': ', '.join(skills)
#             })

#     return data

# def main():
#     chrome_driver_path = "chromedriver.exe"
#     start_page = 1
#     end_page = 1566

#     driver = configure_driver(chrome_driver_path)
#     job_data = scrape_job_data(driver, start_page, end_page)
#     driver.quit()

#     df = pd.DataFrame(job_data)
#     df.to_csv("scraped_data.csv", index=False)
#     print("Scraping completed, and data saved to 'scraped_data.csv'.")

# if __name__ == "__main__":
#     main()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient

def configure_driver(driver_path):
    service = Service(driver_path)
    return webdriver.Chrome(service=service)

def is_relevant_job(job):
    title = job.find('a', class_='title').text.lower()
    try:
        description = job.find('div', class_='job-desc').text.lower()
    except AttributeError:
        description = ''

    return 'python' in title or 'python' in description

def scrape_job_data(driver, start_page, id, collection):
    while True:
        url = f"https://www.naukri.com/python-developer-jobs-{start_page}?k=python%20developer"
        driver.get(url)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_listings = soup.find_all('div', class_='srp-jobtuple-wrapper')

        if not job_listings:
            break

        for job in job_listings:
            if is_relevant_job(job):
                title = job.find('a', class_='title').text
                company = job.find('a', class_='comp-name').text
                experience = job.find('span', class_='exp').text
                salary = job.find('span', class_='sal').text
                location = job.find('span', class_='loc').text
                job_url = job.find('a', class_='title')['href']

                try:
                    skills = [tag.text for tag in job.find('ul', class_='tags-gt').find_all('li', class_='tag-li')]
                except AttributeError:
                    skills = []

                job_data = {
                    'ID': id,
                    'Title': title,
                    'Company': company,
                    'Experience': experience,
                    'Salary': salary,
                    'Location': location,
                    'URL': job_url,
                    'Skills': ', '.join(skills)
                }

                collection.insert_one(job_data)
                id += 1

        start_page += 1

def main():
    chrome_driver_path = "chromedriver.exe"
    start_page, id = 1, 1

    driver = configure_driver(chrome_driver_path)

    # MongoDB setup
    client = MongoClient('mongodb+srv://HSoni:E0RQoRcFRqg4MFOt@joblists.r9yjyat.mongodb.net/?retryWrites=true&w=majority')
    db = client['job_scraping']
    collection = db['job_data_collection']

    scrape_job_data(driver, start_page, id, collection)
    driver.quit()

    print("Scraping completed, and data saved to MongoDB.")

if __name__ == "__main__":
    main()






