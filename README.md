# Next Bus Ekensberg
Application to find and visualize time for the next SL bus leaving from Ekensberg station, Stockholm, Sweden. 

# Todos
1. Update tests with mocks so no api calls needs to be made during development
1. Handle that you only get 10000 calls per month for a 24h active visualization, e.g. don't poll during night, poll smartly when waiting for a bus (i.e. count internally and sync only every 5 minutes for long waits and 1 minute for short waits)
1. Error-handling when no connectivity or bad data
1. Make GUI designed for small screens (2.8)
1. Build hardware
1. Deploy to raspi with external screen