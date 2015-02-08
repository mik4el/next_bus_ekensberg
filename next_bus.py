from config import credentials
import requests
import time
import datetime


class NextBusChecker:
    def __init__(self):
        self.last_data_updated_at = None
        self.last_data_minutes_to_next_bus = None
        self.minutes_to_next_bus = None

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
            sl_time = api_result["ResponseData"]["LatestUpdate"]
        except (KeyError, TypeError):
            return "No data"
        expected_time = datetime.datetime.strptime(expected_time, "%Y-%m-%dT%H:%M:%S")
        sl_time = datetime.datetime.strptime(sl_time, "%Y-%m-%dT%H:%M:%S")
        minutes = (expected_time - sl_time).seconds / 60
        return minutes

    def print_next_bus(self):
        print "Next bus leaves in: %s" % self.minutes_to_next_bus
        return

    def tick(self):
        now = datetime.datetime.now()

        # TODO: update minutes_to_next_bus using now, last_data_minutes_to_next_bus and last_data_updated_at

        if self.last_data_updated_at is not None:
            if (now - self.last_data_updated_at).seconds < 30:
                return

        # TODO: if no bus until time X, don't get new data until time X - 15 minutes

        data = self.get_minutes_to_next_bus()
        if data == "No data":
            return

        self.last_data_updated_at = now
        self.last_data_minutes_to_next_bus = data
        self.minutes_to_next_bus = self.last_data_minutes_to_next_bus
        self.print_next_bus()

    def loop(self):
        while True:
            # tick every second
            self.tick()
            time.sleep(1)


if __name__ == "__main__":
    next_bus_checker = NextBusChecker()
    next_bus_checker.loop()