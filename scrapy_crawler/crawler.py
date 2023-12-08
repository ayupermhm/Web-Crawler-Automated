import scrapy
import csv
from nlp_processing.nlp_processor import nlp_processing
from classification.classifier import classify_page
from extraction.extractor import extract_data
from clean_up.cleaner import clean_up

class MySpider(scrapy.spider):
    name = "my_spider"

    def start_requests(self):
        with open('urls.csv','r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                url = row['url']
                yield scrapy.Request(url=url, callback = self.parse)

    def parse(self, response):
        page_text = response.xpath('//body//text()').getall()
        text = ''.join(page_text)

        nlp_data = nlp_processing(text)
        classified = classify_page(nlp_data)
        extracted_data = extract_data(nlp_data)
        cleaned_data = clean_up(extracted_data)

        yield {
            'url': response.url,
            'text': text,
            'nlp_data': nlp_data,
            'classified': classified,
            'extracted_data': extracted_data,
            'cleaned_data': cleaned_data
        }