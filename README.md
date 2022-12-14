## AppStore Apps Crawler ##


Two mains API endpoints : 
- /<int:n> 
- /<int:n>/json
Both endpoints print the data of the n top apps, one return it as an html, the second one as a json.


To run the API, enter commands: 
- docker build -t flask_app:latest .
- docker run -p 5005:5005 -d flask_app
- go to localhost:5005/<end_point> on your browser.

