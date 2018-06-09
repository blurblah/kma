# KMA
Korea weather information library for kma.go.kr under python3

### Dependencies
This library uses below libraries. Please refer requirements.txt for the details.
1. urllib3
2. certifi
3. pytz

### How to use this library

#### 1. Request to issue a service key
Please visit below url.
You should understand Korean language, I think.

https://www.data.go.kr/dataset/15000099/openapi.do

#### 2. Install
```python
pip install kma
```

#### 3. Sample code
```python
from kma import Weather

w = Weather('YOUR_SERVICE_KEY')
curr = w.get_current()
forecast = w.get_forecast()

print('Current temperature: {}'.format(curr.temperature))
```