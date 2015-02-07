from config import credentials


def minutes_to_next_bus():
    minutes = 0
    print "Accessing Trafiklab using key %s" % credentials.TRAFIKLAB_API_KEY
    return minutes


def print_next_bus():
    print "next bus leaves in: %s" % minutes_to_next_bus()
    return


if __name__ == "__main__":
    print_next_bus()