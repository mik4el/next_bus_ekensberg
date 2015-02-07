from config import credentials
import requests


def minutes_to_next_bus():
    """
    Gets minutes to next bus from Trafiklab Api

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
    #print "Accessing api using url: %s" % api_url

    api_request = requests.get(api_url)

    api_result = api_request.json()
    #print "Result: %s" % api_result

    minutes = api_result["ResponseData"]["Buses"][0]["DisplayTime"]  # Very unsafe

    return minutes


def print_next_bus():
    print "next bus leaves in: %s" % minutes_to_next_bus()
    return


if __name__ == "__main__":
    print_next_bus()