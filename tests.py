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
        self.assertEqual(result, 3)

    def test_minutes_to_next_bus_bus_left(self):
        data = {u'ExecutionTime': 72, u'ResponseData': {u'LatestUpdate': u'2015-02-09T21:14:55', u'Buses': [
            {u'TimeTabledDateTime': u'2015-02-09T21:15:00', u'Destination': u'Liljeholmen', u'DisplayTime': u'Nu',
             u'StopPointNumber': 14066, u'ExpectedDateTime': u'2015-02-09T21:15:00', u'TransportMode': u'BUS',
             u'Deviations': None, u'GroupOfLine': None, u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
             u'LineNumber': u'133', u'StopAreaNumber': 14066, u'StopPointDesignation': None, u'JourneyDirection': 2},
            {u'TimeTabledDateTime': u'2015-02-09T21:30:00', u'Destination': u'Liljeholmen', u'DisplayTime': u'14 min',
             u'StopPointNumber': 14066, u'ExpectedDateTime': u'2015-02-09T21:30:00', u'TransportMode': u'BUS',
             u'Deviations': None, u'GroupOfLine': None, u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
             u'LineNumber': u'133', u'StopAreaNumber': 14066, u'StopPointDesignation': None, u'JourneyDirection': 2},
            {u'TimeTabledDateTime': u'2015-02-09T21:45:00', u'Destination': u'Liljeholmen', u'DisplayTime': u'29 min',
             u'StopPointNumber': 14066, u'ExpectedDateTime': u'2015-02-09T21:45:00', u'TransportMode': u'BUS',
             u'Deviations': None, u'GroupOfLine': None, u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
             u'LineNumber': u'133', u'StopAreaNumber': 14066, u'StopPointDesignation': None, u'JourneyDirection': 2},
            {u'TimeTabledDateTime': u'2015-02-09T22:00:00', u'Destination': u'Liljeholmen', u'DisplayTime': u'22:00',
             u'StopPointNumber': 14066, u'ExpectedDateTime': u'2015-02-09T22:00:00', u'TransportMode': u'BUS',
             u'Deviations': None, u'GroupOfLine': None, u'StopAreaName': u'Ekensberg', u'SiteId': 1600,
             u'LineNumber': u'133', u'StopAreaNumber': 14066, u'StopPointDesignation': None, u'JourneyDirection': 2}],
                                                        u'Ships': [], u'StopPointDeviations': [], u'Trams': [],
                                                        u'DataAge': 20, u'Trains': [], u'Metros': []}, u'Message': None,
                u'StatusCode': 0}
        self.next_bus_checker.get_data_from_api = Mock(return_value=data)
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, 0)

    def test_minutes_to_next_bus_no_bus(self):
        data = {u'ExecutionTime': 72, u'ResponseData': {u'LatestUpdate': u'2015-02-09T21:14:55', u'Buses': [],
                                                        u'Ships': [], u'StopPointDeviations': [], u'Trams': [],
                                                        u'DataAge': 20, u'Trains': [], u'Metros': []},
                u'Message': None, u'StatusCode': 0}
        self.next_bus_checker.get_data_from_api = Mock(return_value=data)
        result = self.next_bus_checker.get_minutes_to_next_bus()
        self.assertEqual(result, "No bus")

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
        self.next_bus_checker.last_data_updated_at = None
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        self.next_bus_checker.tick()
        self.assertIsNotNone(self.next_bus_checker.last_data_updated_at)
        self.assertIsNotNone(self.next_bus_checker.last_data_minutes_to_next_bus)
        self.assertTrue(self.next_bus_checker.bus_is_coming)

    def test_nth_tick_in_wait(self):
        old_data_date = datetime.datetime.now() - datetime.timedelta(seconds=29)
        old_last_data = 10
        self.next_bus_checker.last_data_updated_at = old_data_date
        self.next_bus_checker.last_data_minutes_to_next_bus = old_last_data
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        self.next_bus_checker.tick()
        self.assertEqual(self.next_bus_checker.last_data_updated_at, old_data_date)
        self.assertEqual(self.next_bus_checker.last_data_minutes_to_next_bus, old_last_data)

    def test_nth_tick_after_wait(self):
        old_data_date = datetime.datetime.now() - datetime.timedelta(seconds=31)
        old_last_data = 10
        self.next_bus_checker.last_data_updated_at = old_data_date
        self.next_bus_checker.last_data_minutes_to_next_bus = old_last_data
        self.next_bus_checker.bus_is_coming = True
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        self.next_bus_checker.tick()
        self.assertNotEqual(self.next_bus_checker.last_data_updated_at, old_data_date)
        self.assertNotEqual(self.next_bus_checker.last_data_minutes_to_next_bus, old_last_data)
        self.assertTrue(self.next_bus_checker.bus_is_coming)

    def test_nth_tick_no_bus(self):
        now = datetime.datetime.now()
        self.next_bus_checker.get_now = Mock(return_value=now)
        old_data_date = now - datetime.timedelta(seconds=31)
        old_last_data = 10
        self.next_bus_checker.last_data_updated_at = old_data_date
        self.next_bus_checker.last_data_minutes_to_next_bus = old_last_data
        self.next_bus_checker.bus_is_coming = True
        data = {u'ExecutionTime': 72, u'ResponseData': {u'LatestUpdate': u'2015-02-09T21:14:55', u'Buses': [],
                                                        u'Ships': [], u'StopPointDeviations': [], u'Trams': [],
                                                        u'DataAge': 20, u'Trains': [], u'Metros': []},
                u'Message': None, u'StatusCode': 0}
        self.next_bus_checker.get_data_from_api = Mock(return_value=data)
        self.next_bus_checker.tick()
        self.assertEqual(self.next_bus_checker.last_data_updated_at, now)
        self.assertIsNone(self.next_bus_checker.last_data_minutes_to_next_bus)
        self.assertFalse(self.next_bus_checker.bus_is_coming)

    def test_nth_tick_with_nodata(self):
        old_data_date = datetime.datetime.now() - datetime.timedelta(seconds=31)
        old_last_data = 10
        self.next_bus_checker.last_data_updated_at = old_data_date
        self.next_bus_checker.last_data_minutes_to_next_bus = old_last_data
        self.next_bus_checker.get_data_from_api = Mock(return_value=GOOD_API_DATA)
        self.next_bus_checker.get_minutes_to_next_bus = Mock(return_value="No data")
        self.next_bus_checker.tick()
        self.assertEqual(self.next_bus_checker.last_data_updated_at, old_data_date)
        self.assertEqual(self.next_bus_checker.last_data_minutes_to_next_bus, old_last_data)

    def test_update_minutes_to_next_bus(self):
        now = datetime.datetime.now()
        self.next_bus_checker.get_now = Mock(return_value=now)
        self.next_bus_checker.last_data_updated_at = now - datetime.timedelta(seconds=59, minutes=3)
        self.next_bus_checker.last_data_minutes_to_next_bus = 11
        self.next_bus_checker.recalculate_minutes_to_next_bus()
        self.assertEqual(self.next_bus_checker.minutes_to_next_bus, 8)
        self.next_bus_checker.last_data_updated_at = now - datetime.timedelta(seconds=01, minutes=3)
        self.next_bus_checker.last_data_minutes_to_next_bus = 11
        self.next_bus_checker.recalculate_minutes_to_next_bus()
        self.assertEqual(self.next_bus_checker.minutes_to_next_bus, 8)
        self.next_bus_checker.last_data_updated_at = now - datetime.timedelta(seconds=59, minutes=0)
        self.next_bus_checker.last_data_minutes_to_next_bus = 11
        self.next_bus_checker.recalculate_minutes_to_next_bus()
        self.assertEqual(self.next_bus_checker.minutes_to_next_bus, 11)
        self.next_bus_checker.last_data_updated_at = now - datetime.timedelta(seconds=1, minutes=0)
        self.next_bus_checker.last_data_minutes_to_next_bus = 11
        self.next_bus_checker.recalculate_minutes_to_next_bus()
        self.assertEqual(self.next_bus_checker.minutes_to_next_bus, 11)

        # Check what happens if bus has left
        self.next_bus_checker.last_data_updated_at = now - datetime.timedelta(seconds=0, minutes=10)
        self.next_bus_checker.last_data_minutes_to_next_bus = 5
        self.next_bus_checker.recalculate_minutes_to_next_bus()
        self.assertEqual(self.next_bus_checker.minutes_to_next_bus, 0)