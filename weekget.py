import requests as rs
import bs4

def get_7day_data(url):

    if url == "javascript:void(0);":
        return {}

    res = rs.get(url)
    res.encoding = 'utf-8'
    res.raise_for_status()

    s = bs4.BeautifulSoup(res.text,'html.parser')
    day_tags = s.select('ul[class="t clearfix"] > li')
    print(f'查到日期标签{len(day_tags)}个')


    week_weather_info = {}
    for day in day_tags:
        day_info = {}
        text = str(day)
        soup = bs4.BeautifulSoup(text,'html.parser')
        
        day_info['天气'] = soup.select("p[class='wea']")[0].getText()       
        if soup.select("p[class='tem'] > span") == []:
            tem = soup.select("p[class='tem'] > i")[0].getText()
            day_info['温度'] = tem
        else:
            top = soup.select("p[class='tem'] > span")[0].getText()
            low = soup.select("p[class='tem'] > i")[0].getText()
            day_info['温度'] = f'{low[:-1]}-{top}'
            
        win = soup.select("p[class='win'] > em > span")
        little_wins = [span.get('title') for span in win]
        win_lv = soup.select("p[class='win'] > i")
        day_info['风向'] = ','.join(little_wins)
        day_info['风力'] = win_lv[0].getText()

        date = soup.select("h1")[0].getText()
        week_weather_info[date] = day_info
    return week_weather_info

#url = "https://www.weather.com.cn/weather/101250107.shtml#search"
url = "https://www.weather.com.cn/weather/101010100.shtml#search"
week = get_7day_data(url)
print('北京未来一周天气：')
for day,data in week.items():
    print(f'{day}:  {data['温度']}  {data['天气']}  {data['风向']}')