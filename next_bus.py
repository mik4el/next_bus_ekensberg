from config import credentials
import requests
import time
import datetime
import threading


class NextBusChecker(threading.Thread):
    def __init__(self):
        super(NextBusChecker, self).__init__()
        self.last_data_updated_at = None
        self.last_data_minutes_to_next_bus = None
        self.minutes_to_next_bus = None
        self.bus_is_coming = False

    def get_data_from_api(self):
        """
        Gets data from Trafiklab Api

        Api call format:
        https://api.sl.se/api2/realtimedepartures.json?key=<TRAFIKLAB_API_KEY>&siteid=<SITEID>&timewindow=<TIMEWINDOW>
        SITEID for Ekensberg is 1600 (2015-02-07)
        TIMEWINDOW is integer for minutes from now, max is 60.

        Api call for Ekensberg for 60 minutes:
        https://api.sl.se/api2/realtimedepartures.json?key=<TRAFIKLAB_API_KEY>&siteid=1600&timewindow=60

        Example response:
        {
            "StatusCode": 0,
            "Message": null,
            "ExecutionTime": 50,
            "ResponseData": {
                "LatestUpdate": "2015-02-07T22:35:44",
                "DataAge": 15,
                "Metros": [],
                "Buses": [
                    {
                        "JourneyDirection": 2,
                        "GroupOfLine": null,
                        "StopAreaName": "Ekensberg",
                        "StopAreaNumber": 14066,
                        "StopPointNumber": 14066,
                        "StopPointDesignation": null,
                        "TimeTabledDateTime": "2015-02-07T23:00:00",
                        "ExpectedDateTime": "2015-02-07T23:00:00",
                        "DisplayTime": "24 min",
                        "Deviations": null,
                        "TransportMode": "BUS",
                        "LineNumber": "133",
                        "Destination": "Liljeholmen",
                        "SiteId": 1600
                    },
                    {
                        "JourneyDirection": 2,
                        "GroupOfLine": null,
                        "StopAreaName": "Ekensberg",
                        "StopAreaNumber": 14066,
                        "StopPointNumber": 14066,
                        "StopPointDesignation": null,
                        "TimeTabledDateTime": "2015-02-07T23:30:00",
                        "ExpectedDateTime": "2015-02-07T23:30:00",
                        "DisplayTime": "23:30",
                        "Deviations": null,
                        "TransportMode": "BUS",
                        "LineNumber": "133",
                        "Destination": "Liljeholmen",
                        "SiteId": 1600
                    }
                ],
                "Trains": [],
                "Trams": [],
                "Ships": [],
                "StopPointDeviations": []
            }
        }
        """

        api_url = "https://api.sl.se/api2/realtimedepartures.json?key=%s&siteid=1600&timewindow=60" % credentials.TRAFIKLAB_API_KEY

        try:
            api_request = requests.get(api_url, timeout=10)
        except:
            api_result = "No data"
        else:
            api_result = api_request.json()

        return api_result

    def get_minutes_to_next_bus(self):
        """
        Gets minutes to next bus
        """
        api_result = self.get_data_from_api()
        print api_result
        try:
            expected_time = api_result["ResponseData"]["Buses"][0]["ExpectedDateTime"]
            latest_update = api_result["ResponseData"]["LatestUpdate"]
            data_age = api_result["ResponseData"]["DataAge"]
        except (KeyError, TypeError):
            return "No data"
        except IndexError:
            return "No bus"

        expected_time = datetime.datetime.strptime(expected_time, "%Y-%m-%dT%H:%M:%S")
        latest_update = datetime.datetime.strptime(latest_update, "%Y-%m-%dT%H:%M:%S")
        sl_time = latest_update + datetime.timedelta(seconds=data_age)
        if expected_time > sl_time:
            minutes = (expected_time - sl_time).seconds / 60
        else:
            minutes = 0
        return minutes

    def print_next_bus(self):
        if self.last_data_updated_at is None:
            print "Getting data"
            return
        if self.bus_is_coming:
            print "Next bus leaves in: %s minutes (%s, data from: %s)" % (
                self.minutes_to_next_bus, self.get_now(), self.last_data_updated_at)
        else:
            print "No bus in data (%s, data from: %s)" % (self.get_now(), self.last_data_updated_at)

    def get_now(self):
        return datetime.datetime.now()

    def recalculate_minutes_to_next_bus(self):
        # Check data
        if self.last_data_updated_at is None:
            self.minutes_to_next_bus = None
            return
        if self.last_data_minutes_to_next_bus is None:
            self.minutes_to_next_bus = None
            return

        # When no data recorded, don't recalculate
        if self.last_data_updated_at is None:
            return
        minutes_since_update = (self.get_now() - self.last_data_updated_at).seconds / 60
        if self.last_data_minutes_to_next_bus - minutes_since_update > 0:
            self.minutes_to_next_bus = self.last_data_minutes_to_next_bus - minutes_since_update
        else:
            self.minutes_to_next_bus = 0

    def tick(self):
        now = self.get_now()

        self.recalculate_minutes_to_next_bus()

        self.print_next_bus()

        # Check if data should be updated
        if self.last_data_updated_at is not None:
            if (now - self.last_data_updated_at).seconds < 30:
                return

        if self.minutes_to_next_bus > 10:
            return

        if not self.bus_is_coming and self.last_data_updated_at is not None:
            if (now - self.last_data_updated_at).seconds < 1800:
                return

        # Update and handle data
        data = self.get_minutes_to_next_bus()

        if data == "No data":
            # Don't update data
            return

        if data == "No bus":
            self.last_data_updated_at = now
            self.last_data_minutes_to_next_bus = None
            self.bus_is_coming = False
        else:
            self.last_data_updated_at = now
            self.last_data_minutes_to_next_bus = data
            self.bus_is_coming = True

    def run(self):
        while True:
            # tick every second
            self.tick()
            time.sleep(1)


if __name__ == "__main__":
    next_bus_checker = NextBusChecker()
    next_bus_checker.start()