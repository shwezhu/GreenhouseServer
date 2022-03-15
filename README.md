# An IoT Server Based on MQTT and HTTP
#### 1. An HTTP server implemented in Python socket programming based on multiplexing

Accept a specified HTTP request and response corresponding data that stored in Database.

e.g.,
```shell
curl -X GET -H "sql: select * from temperature" http://127.0.0.1:8080

{"results": [{"temperature": 26.3, "time": "2022-03-09 15:13"}, {"temperature": 26.3, "time": "2022-03-09 16:04"}, {"temperature": 26.3, "time": "2022-03-09 16:06"}, {"temperature": 28.3, "time": "2022-03-09 18:30"}]}
```

#### 2. Store data from MQTT clients into Database

