# import time # TODO: time import is here if we need to check time scaling at line 72
from urllib.request import urlopen as request  # url request
from bs4 import BeautifulSoup as Soup  # web scraper

from FileManager import ExcelParser  # file operations

import concurrent.futures  # fasten the process by multithreading

MAX_THREADS = 30  # limit the number of threads


# if the availability definition changes, this method will be modified
def get_availability(all_models, disabled):
    if all_models == 0:
        return 0
    return (all_models - disabled) * 100 // all_models


# .body.div#ProductPage.product-content-wrapper.product-detail-container.row.product__wrapper.product__content
def get_product_info(url):
    # request the page and close the client
    client = request(url)
    page_html = client.read()
    client.close()

    # parse the page to get attributes
    page_soup = Soup(page_html, "html.parser")

    # get the required information
    code = page_soup.find("div", attrs={"class": "product__code"})
    brand = page_soup.find("a", attrs={"class": "product__brand"})
    name = page_soup.find("h1", attrs={"class": "product__title"})
    price = page_soup.find("div", attrs={"class": "product__price"})

    # unavailable products has disabled class along their anchor tag
    availability_all = page_soup.findAll("a", attrs={"class": "product__size-variant"})
    availability_disabled = page_soup.findAll("a", attrs={"class": "d-flex align-items-center justify-content-center "
                                                                   "text-reset product__variant product__size-variant"
                                                                   " mb-3 js-variant disabled"})
    # calculate rounded availability
    availability = get_availability(len(availability_all), len(availability_disabled))

    return code, brand, name, price, availability


def multithreading(parser, urls):
    threads = min(MAX_THREADS, len(urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for link_idx, result in enumerate(executor.map(get_product_info, urls)):
            code, brand, name, price, availability = result[0], result[1], result[2], result[3], result[4]
            parser.save_to_file(link_idx + 2, code, brand, name, price, availability)


# Report File is formatted as below:
# Code| Brand | Name | Price | Availability
def main():
    website = "https://www.spx.com.tr"
    data_file_name = "Product Detail URL.xlsx"
    data_sheet_name = "Sheet4"

    report_file_name = "Report.xlsx"
    report_sheet_name = "Report"

    # get product links from file
    parser = ExcelParser(data_file_name, report_file_name, report_sheet_name)
    product_links = parser.get_links(website, data_sheet_name)

    # crate report sheet and place the titles
    parser.create_report_file()

    # to test the time scaling with size
    # t0 = time.time()
    multithreading(parser, product_links)
    # t1 = time.time()
    # print(f"{t1 - t0} seconds to download {len(product_links)} stories.")

    parser.close_report_file()


main()
