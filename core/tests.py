from rest_framework.exceptions import ParseError
from rest_framework.test import APITestCase
import unittest

class PeriodValidator(unittest.TestCase):

    def setUp(self):
        from validation import validated_period
        self.validated_period = validated_period

    def test_exception_string(self):
        with self.assertRaises(ParseError):
            self.validated_period('elephant')

    def test_exception_negative(self):
        with self.assertRaises(ParseError):
            self.validated_period(-3)

    def test_exception_out_of_range(self):
        with self.assertRaises(ParseError):
            self.validated_period(17)

    def test_pass(self):
        self.assertEqual(self.validated_period(3), 3)


class WeatherEndpoint(APITestCase):
    def setUp(self):
        from rest_framework import status
        self.status = status
        from rest_framework.test import APIRequestFactory
        self.factory = APIRequestFactory()

    def test_valid(self):
        response = self.client.get('/London/3/')
        self.assertEqual(response.status_code, self.status.HTTP_200_OK)

    def test_redirect(self):
        response = self.client.get('/London/3')
        self.assertEqual(response.status_code, self.status.HTTP_301_MOVED_PERMANENTLY)

    def test_invalid(self):
        response = self.client.get('///')
        self.assertEqual(response.status_code, self.status.HTTP_404_NOT_FOUND)

class BuildURL(unittest.TestCase):
    def setUp(self):
        from validation import build_url
        import testdata
        self.pass_city = "London"
        self.correct_url = testdata.correct_url
        self.pass_period = 3
        self.fail_city = 3
        self.build_url = build_url

    def test_builds_correctly(self):
        #this is a pretty ugly test.
        self.assertEqual(self.build_url(self.pass_city, self.pass_period), self.correct_url)

    def test_invalid(self):
        with self.assertRaises(TypeError):
            self.build_url(self.fail_city,"London")
