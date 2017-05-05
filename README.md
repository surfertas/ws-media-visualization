Media Content Visualization
---

Small web-service that allows user to upload video (.mov) file and create a
motion flow visualization using computer vision techniques.

### Note:
- This was just an exercise to understand some of the workflow involved in
  created a web service.

### Usage:
```
git clone https://github.com/surfertas/ws-media-visualization.git
docker build -t ol-motionflow .
docker run -p 5050:5050 ol-motionflow
```

### Todo:
- Need to add database capabilities for user and pw handling. Currently to
  login, set username == password.
- Need to create config file.

