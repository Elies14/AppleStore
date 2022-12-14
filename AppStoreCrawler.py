import requests
import json
import regex as re
from bs4 import BeautifulSoup


class AppStoreCrawler:
    itunes_url = 'http://rss.applemarketingtools.com/api/v2/us/apps/top-free/{}/apps.json'
    app_url = 'https://apps.apple.com/us/app/id'

    def __init__(self):
        self.session = requests.Session()
        self.soup = BeautifulSoup('<title></title>', "html.parser")

    def get_top_apps(self, n: int):
        """
        :param n: Number of applications to get
        :return: A list of n tuples, each tuple contains the ID and the name of the application
        """
        response = self.session.get(self.itunes_url.format(n))
        results = json.loads(response.content).get('feed', {}).get('results')
        return [(result['id'], result['name']) for result in results] if results else None

    def navigate_to_page(self, data: dict):
        """
        Update beautiful soup to be on the AppStore's page of app {id}
        :param data: dict with the app_id and the app_name
        :return:
        """
        while not self.soup.find('title') or data['name'] not in self.soup.find('title').text:
            response = self.session.get(self.app_url + data['id'])
            self.soup = BeautifulSoup(response.content, "html.parser")

    def get_data_from_url(self, data: dict):
        rating = self.get_text_by_class('we-customer-ratings__averages__display')
        number_of_rating = self.get_text_by_class('we-customer-ratings__count')
        data.update({'rating': rating if rating else None,
                     'number_of_rating': number_of_rating.split()[0] if number_of_rating else None})
        self.update_informations(data)

    def update_informations(self, data: dict):
        """
        :param data: The dictionary with all the data about the application
        :return: Change data in place, update all the data found in Information Section
        """
        infos = self.soup.find_all(class_='information-list__item')
        data.update({info.find('dt').text.strip().lower(): info.find('dd').text.strip() for info in infos})
        self.update_app_type(data)

        data['min_age'] = self.find_number(data.get('age rating'), int)
        data['is_kids_friendly'] = data['min_age'] < 18 if data['min_age'] else None
        data['in_app_purchases'] = data.get('in-app purchases')
        self.update_compatibility_version(data)
        self.update_subscriptions(data)

    def update_subscriptions(self, data):
        subscriptions_info = data.get('in-app purchases')
        if subscriptions_info:
            for time in ['weekly', 'monthly', 'yearly']:
                prices = subscriptions_info.lower().split(time)
                if len(prices) > 1:
                    price = self.find_number(prices[1])
                    data.update({f'{time}_sub': price})

    def get_text_by_class(self, class_name: str):
        """
        :return: Find element by class name and return the text contained in this element.
        """
        element = self.soup.find_all(class_=class_name)
        return element[0].text if element else ''

    @staticmethod
    def update_app_type(data: dict):
        """
        :param data: The dictionary with all the data about the application
        :return: Update data dictionary in place - change the app type according to category.
        """
        types = ['tv', 'photo', 'music', 'game']
        data.update({f'is_{t}_app': False for t in types})
        data.update({next((f'is_{k}_app' for k in types if k in data.get('category', '').lower()), 'other'): True})
        if data.get('other'):
            other = data.get('category', '')
            data['other'] = other.split()[0] if other else None

    def update_compatibility_version(self, data: dict):
        """
        Change data dictionary in place, update compatibility information.
        :param data:
        :return:
        """
        versions = self.soup.find_all(class_='information-list__item__definition__item')
        data.update({f'min_{version.find("dt").text.strip().lower()}_version': self.find_number(version.find('dd').text)
                     for version in versions})

    @staticmethod
    def find_number(s: str, type=float):
        """

        :param s: String to find the number
        :param type: either float or int - type of the output
        :return:
        """
        if s:
            n = re.findall('\d+\.?\d*', s)
            return type(n[0]) if n else None
