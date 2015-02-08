import unittest
from next_bus import NextBusChecker
from mock import Mock
import datetime


GOOD_API_DATA = {u"ExecutionTime": 92,
                 u'ResponseData': {u'LatestUpdate': u'2015-02-08T17:10:50', u'Buses': [
                     {u'TimeTabledDateTime': u'2015-02-08T17:15:00',
                      u'Destination': u'Liljeholmen', u'DisplayTime': u'3 min',
                      u'StopPointNumber': 14066,
                      u'ExpectedDateTime': u'2015-02-08T17:15:00',
                      u'TransportMode': u'BUS', u'Deviations': None, u'GroupOfLine': None,
                      u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
                      u'LineNumber': u'133', u'StopAreaNumber': 14066,
                      u'StopPointDesignation': None, u'JourneyDirection': 2},
                     {u'TimeTabledDateTime': u'2015-02-08T17:30:00',
                      u'Destination': u'Liljeholmen', u'DisplayTime': u'18 min',
                      u'StopPointNumber': 14066,
                      u'ExpectedDateTime': u'2015-02-08T17:30:00',
                      u'TransportMode': u'BUS', u'Deviations': None, u'GroupOfLine': None,
                      u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
                      u'LineNumber': u'133', u'StopAreaNumber': 14066,
                      u'StopPointDesignation': None, u'JourneyDirection': 2},
                     {u'TimeTabledDateTime': u'2015-02-08T17:45:00',
                      u'Destination': u'Liljeholmen', u'DisplayTime': u'17:45',
                      u'StopPointNumber': 14066,
                      u'ExpectedDateTime': u'2015-02-08T17:45:00',
                      u'TransportMode': u'BUS', u'Deviations': None, u'GroupOfLine': None,
                      u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
                      u'LineNumber': u'133', u'StopAreaNumber': 14066,
                      u'StopPointDesignation': None, u'JourneyDirection': 2},
                     {u'TimeTabledDateTime': u'2015-02-08T18:00:00',
                      u'Destination': u'Liljeholmen', u'DisplayTime': u'18:00',
                      u'StopPointNumber': 14066,
                      u'ExpectedDateTime': u'2015-02-08T18:00:00',
                      u'TransportMode': u'BUS', u'Deviations': None, u'GroupOfLine': None,
                      u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
                      u'LineNumber': u'133', u'StopAreaNumber': 14066,
                      u'StopPointDesignation': None, u'JourneyDirection': 2}],
                                   u'Ships': [], u'StopPointDeviations': [], u'Trams': [],
                                   u'DataAge': 13, u'Trains': [], u'Metros': []},
                 u'Message': None, u'StatusCode': 0}


class TestMinutesToNextBus(unittest.TestCase):
    def setUp(self):
        self.next_bus_checker = NextBusChecker()

    def test_minutes_to_next_bus_standard_api_call(self):
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, "3 min")

    def test_minutes_to_next_bus_error_in_api_result(self):
        self.next_bus_checker.get_data_from_api = Mock(return_value={})
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, "No data")
        self.next_bus_checker.get_data_from_api = Mock(return_value=[])
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, "No data")
        self.next_bus_checker.get_data_from_api = Mock(return_value="")
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, "No data")
        self.next_bus_checker.get_data_from_api = Mock(return_value="No data")
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, "No data")

    def test_first_tick(self):
        # when no last_data_updated_at, check for data and
        self.next_bus_checker.last_data_updated_at = None
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        self.next_bus_checker.tick()
        self.assertIsNotNone(self.next_bus_checker.last_data_updated_at)
        self.assertIsNotNone(self.next_bus_checker.last_data_minutes_to_next_bus)

    def test_nth_tick(self):
        # when no last_data_updated_at, check for data and
        old_data_date = datetime.datetime.now() - datetime.timedelta(seconds=29)
        old_last_data = 10
        self.next_bus_checker.last_data_updated_at = old_data_date
        self.next_bus_checker.last_data_minutes_to_next_bus = old_last_data
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        self.next_bus_checker.tick()
        self.assertEqual(self.next_bus_checker.last_data_updated_at, old_data_date)
        self.assertEqual(self.next_bus_checker.last_data_minutes_to_next_bus, old_last_data)
