import unittest

from AppStoreCrawler import AppStoreCrawler


class TestCrawler(unittest.TestCase):

    """
    Those unittest will check that the crawler class is working for Amazon Prime Video application id : 545519333
    """
    def setUp(self) -> None:
        self.crawler = AppStoreCrawler()
        self.data = {'id': '545519333', 'name': 'Amazon Prime Video'}
        self.crawler.navigate_to_page(self.data)
        self.wrong_crawler = AppStoreCrawler()
        self.wrong_data = {'id': 'error', 'name': 'error_name'}

    def test_get_top_apps(self):
        top_apps = self.crawler.get_top_apps(10)
        self.assertEqual(len(top_apps), 10)
        [self.assertTrue(app[0].isnumeric()) for app in top_apps]

    def test_get_top_apps_None(self):
        self.assertIsNone(self.crawler.get_top_apps('not int'))

    def test_get_text_by_class_ok(self):
        title = self.crawler.get_text_by_class('product-header__title')
        self.assertIn(self.data['name'], title)

    def test_get_text_by_class_not_exist(self):
        text = self.crawler.get_text_by_class('imaginary-class')
        self.assertEqual(text, '')

    def test_update_informations_ok(self):
        expected_data = {'id': '545519333', 'name': 'Amazon Prime Video', 'seller': 'AMZN Mobile LLC', 'size': '63 MB',
                         'category': 'Entertainment', 'price': 'Free',
                         'is_tv_app': False, 'is_photo_app': False, 'is_music_app': False, 'is_game_app': False,
                         'other': 'Entertainment', 'min_age': 12, 'is_kids_friendly': True, 'min_iphone_version': 14.0,
                         'min_ipad_version': 14.0, 'min_mac_version': 11.4, 'min_apple tv_version': 14.3}
        self.crawler.update_informations(self.data)
        self.assertEqual(self.data, self.data | expected_data)
        self.assertIsNotNone(self.data.get('languages'))

    def test_update_subscritpions_ok(self):
        data = {'in-app purchases': 'Prime Video Monthly\n$8.99\n\n\n'
                                    'Prime Video Weekly\n$1.99 Monthly\n$8.99 Yearly\n$99.99'}
        expected_data = {'weekly_sub': 1.99, 'monthly_sub': 8.99, 'yearly_sub': 99.99}
        self.crawler.update_subscriptions(data)
        self.assertEqual(data, data | expected_data)

    def test_update_no_subcriptions(self):
        data = {'in-app purchases': 'Prime Video 10.99'}
        expected_data = {'weekly_sub': None, 'monthly_sub': None, 'yearly_sub': None}
        self.crawler.update_subscriptions(data)
        [self.assertIsNone(data.get(f'{time}_sub')) for time in ['weekly', 'monthly', 'yearly']]

    def test_update_informations_None(self):
        data = {}
        self.wrong_crawler.update_informations({})
        self.assertEqual(data, {})

    def test_update_compatibility_version_ok(self):
        self.crawler.update_compatibility_version(self.data)
        self.assertEqual(self.data.get('min_iphone_version'), 14.0,
                         f'Wrong iPhone version {self.data.get("min_iPhone_version")} != 14.0')
        self.assertEqual(self.data.get('min_ipad_version'), 14.0,
                         f'Wrong iPad version {self.data.get("min_iPad_version")} != 14.0')
        self.assertEqual(self.data.get('min_mac_version'), 11.4,
                         f'Wrong Mac version {self.data.get("min_mac_version")} != 11.4')

    def test_update_app_type_entertainment(self):
        data = {'category': 'Entertainment'}
        self.helper_app_type(wrong_types=['tv', 'game', 'music', 'photo'], right_type='other',
                             data=data)
        self.assertEqual(data.get('other'), 'Entertainment', f'Wrong type {data.get("other")} != Entertainment')

    def test_update_app_type_photo(self):
        self.helper_app_type(wrong_types=['tv', 'game', 'music'], right_type='photo',
                             data={'category': 'Photo & Video'})

    def test_update_app_type_music(self):
        self.helper_app_type(wrong_types=['tv', 'photo', 'game'], right_type='music',
                             data={'category': 'Music'})

    def test_update_app_type_game(self):
        self.helper_app_type(wrong_types=['tv', 'photo', 'music'], right_type='game',
                             data={'category': 'Games'})

    def test_update_app_type_tv(self):
        self.helper_app_type(wrong_types=['game', 'photo', 'music'], right_type='tv',
                             data={'category': 'TV & Entertainment'})

    def helper_app_type(self, wrong_types, right_type, data):
        self.crawler.update_app_type(data)
        [self.assertFalse(data.get(f'is_{t}_app'), f'This app is not a {t} type') for t in wrong_types]
        if right_type != 'other':
            self.assertTrue(data.get(f'is_{right_type}_app'), f'App should be a {right_type} app')
            self.assertIsNone(data.get('other'))

    def test_update_compatibility_version_empty_data(self):
        self.wrong_crawler.update_compatibility_version(self.wrong_data)
        [self.assertIsNone(self.wrong_data.get(f'min_{device}_version')) for device in ['iphone', 'ipad', 'mac']]

    def test_get_data_from_url_ok(self):
        self.crawler.get_data_from_url(self.data)
        self.assertEqual(self.data, self.data | {'number_of_rating': '13.9M', })

    def test_find_number_ok(self):
        self.assertEqual(self.crawler.find_number('find number 15.4 !'), 15.4)

    def test_find_number_none_result(self):
        self.assertIsNone(self.crawler.find_number('No number in this string!'))
