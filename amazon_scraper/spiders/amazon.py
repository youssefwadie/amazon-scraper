import scrapy
from urllib.parse import urlencode, urljoin
import re
import json

queries = ["gaming laptop",
           "smart tv"]


def to_ascii(string: str) -> str:
    return string.encode('ascii', 'ignore').decode('ascii').strip()


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'dnt': '1',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    def start_requests(self):
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f'https://www.amazon.com/dp/{asin}'
            yield scrapy.Request(url=product_url, callback=self.parse_product_page,
                                 meta={'asin': asin})

        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com", next_page)
            yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_product_page(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
        image = re.search('"large":"(.*?)"', response.text).groups()[0]
        price = response.xpath(
            '//*[(@id = "corePriceDisplay_desktop_feature_div")]//*[contains(concat( " ", @class, " " ), concat( " ", "a-price-whole", " " ))]/text()').extract_first()
        list_price = response.xpath(
            '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[1]/text()').extract_first()

        temp = response.xpath('//*[@id="twister"]')

        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])

        details = {}

        details_section = response.xpath('//*[@id="poExpander"]/div[1]/div/table/tr')
        for entry in details_section:
            details[entry.xpath(".//td[1]/span/text()").extract_first().strip()] = entry.xpath(
                ".//td[2]/span/text()").extract_first().strip()

        information_table = response.xpath('//*[@id="productDetails_techSpec_section_2"]/tr')
        weight = None
        dimensions = None

        for entry in information_table:
            entry_text = entry.xpath(
                ".//*[contains(@class, 'prodDetSectionEntry')]/text()").extract_first()
            if entry_text is None:
                continue
            if 'Weight' in entry_text:
                weight = entry.xpath(".//*[contains(@class, 'prodDetAttrValue')]/text()").extract_first()
            elif 'Dimensions' in entry_text:
                dimensions = entry.xpath(".//*[contains(@class, 'prodDetAttrValue')]/text()").extract_first()

        dimensions_json = {}
        if dimensions is not None:
            dimensions = to_ascii(dimensions).split('x')
            dimensions_json = {
                'length': float(dimensions[0].strip()),
                'width': float(dimensions[1].strip()),
                'height': float(dimensions[2].split('inches')[0].strip())
            }

        if weight is not None:
            weight = float(''.join(filter(lambda ch: ch.isdigit() or ch == '.', weight.strip())))

        images_div = response.xpath('//*[@id="altImages"]//img/@src').extract()
        images = set(filter(lambda img: not re.match('.*\\.gif', img), images_div))

        features = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        if features is not None:
            features = list(map(lambda feature: to_ascii(str(feature)),
                                filter(lambda feature: feature.strip(), features)))

        yield {'asin': asin, 'title': title, 'main_image': image,
               'price': price, 'sizes': sizes, 'colors': colors, 'details': details, 'features': features,
               'list_price': list_price, 'images': images, 'dimensions': dimensions_json, 'weight': weight}
