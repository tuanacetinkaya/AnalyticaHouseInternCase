# AnalyticaHouseInternCase
Summer internship application challenge for applicants. Main goal is to use web scraping in python to gather data from given set of product links. 

## Used Tech-Stack
### openpyxl
For reading and manipulating excel documents.
```
sudo pip3 install openpyxl
```

### BeautifulSoup from bs4
To scrape html freely
```
sudo pip3 install bs4
```

### urlopen from urllib.request
To request and open product websites

### concurrent.futures
For fasten the scraping process by using multithreading


## Case Challenges for Me
#### 1. Choosing library to read from excel
Initially I was planning to use xlrd and xlwt libraries for these operations however the latest version of xlrd (2.0.1) only supports .xls files 
and using previous (1.2.0) version may cause security leaks as it is 
#### 2. Fastening the process as it scales up
Fundamentally making requests and waiting for each of them to respond takes about half a second each and increaseing the number of samples in data set will end up with an hour waiting. It took me some time to research an effective way to handle that.

## What I've learned
Multithreading is an amazing way to handle great number of requests. I realized the way I did it before was the equivalent of my grandmother typing with one finger. Computers has way more process power than handling requests one at a time*. Also python excel handling libraries are a mess and we should be thankful for the developers of pandas and openpyxl.

( * credits to: [Nick Becker](https://beckernick.github.io/faster-web-scraping-python/) )

## Questionaire
### If I’d have 10000 urls that I should visit, then it takes hours to finish. What can we make to fasten this process?
  As a standard scaping process making requests one by one for 10000 urls is unnecessarily slow, so instead we can create multithreads and handle multiple requests at once to fasten the process significantly (%86.4) faster as shown below

##### Without Multithreading
[Check Console Output](https://prnt.sc/yz62sn)
```
145.3196849822998 seconds to download 100 products
```

##### With Multithreading
[Check Console Output](https://prnt.sc/yz65z1)
```
19.78730797767639 seconds to download 100 products
```
  
### Please briefly explain what is API and how it works
API is an abstract interface to communicate with other application's attributes and dataflows, in another words their back-ends, without having to reach their source code and database. Normally applications store their data in physical servers and we need to access these in order to trade and read data from them. However that would endanger the application since it would be possible for anyone to mess with the datas and corrupt files. At that stage, an API access these servers on our behalf and secures the database from misusage of accessors by handling the data flow. 
