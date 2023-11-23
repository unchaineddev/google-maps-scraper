# Google Maps Scraper

This scrapes company information from Google Maps using selenium and Python


## After cloning the repository

- Install the latest chromedriver from: https://googlechromelabs.github.io/chrome-for-testing/ 
- Save it in the root directory.

## How to Run?

### Step 1

Save all the keywords in the ```'io_folder'```

#### Recommended:

- use the right keywords to scrape the information 
- the typical format for accurate results is: ``company name, city, state``


### Step 2

Run the file named ``main.py``

The result will be saved in the ``io_folder`` with the file named ``file.csv``

## How to scrape data without the browser opening?

- Un-comment this line

``# options.add_argument('--headless')``

## How many parallel processes?

- By default, there are 15 processes. You can increase or decrease it as per your requirements. 

To do this change this line:

```python
num_processes = 15     # change this line
# """rest of the code"""
``` 

## What if Connection is insecure?

If connection is insecure, you likely need to update the ``ca.rt`` certificate, which is in the ``security_certificate/`` folder.

Steps:

1. Download the certificate using this [link](https://github.com/wkeeling/selenium-wire/raw/master/seleniumwire/ca.crt)
2. Open chrome > settings > privacy and security
3. Scroll down and click on 'Manage device certificates'
4. Selected 'Trusted Root Certificates'
5. Import the downloaded file and click finish. 