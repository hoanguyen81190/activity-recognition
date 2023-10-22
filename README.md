# Python repository for activity-recognition
## How to run
This is the temporary solution before setting up MQTT connection
1. Start the python server
  python app.py

2. Expose the flask app to netlify 
Use ngrok to foward the request from netlify to out local server at port 5999
  ngrok http 5999

Copy the forwarding URL and paste it to the address in the gyroscope-app. An example
Forwarding                    https://184b-178-232-100-70.ngrok.io 

The ngrok session will be expired after a while. Check if this is the case when having error. If it is, reset ngrok session

3. Data will be saved into folder ./data
