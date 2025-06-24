import requests as rs
import bs4,json

def get_7day_data(url):

    if url =="javascript:void(0);" :
        return {}

    res = rs.get(url)
    res.encoding = 'utf-8'
    res.raise_for_status()

    s = bs4.BeautifulSoup(res.text,'html.parser')
    day_tags = s.select('ul[class="t clearfix"] > li')

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
        well_date = date[:3] +'('+date[4:6] + ')'
        week_weather_info[well_date] = day_info
    return week_weather_info

"""主程序"""
with open('天气数据/urls.json','r',encoding='utf-8')as f:
    content = f.read()
    data = json.loads(content)

sup_city = ['北京','上海','天津','重庆']#
weatherall = {}
i = 0
for k,v in data.items():
    i += 1
    j = 0
    weatherall[k] ={}
    if k in sup_city:
        for area,url in v.items():
            j += 1
           
            if len(url) == 58:
                real_url = "http://www.weather.com.cn/weather/"+url[-22:-13] +'.shtml#search'
            else:
                real_url = 0
            weatherall[k][area] = get_7day_data(real_url)

            print(f"{k}({i}/{len(data)})  {area}({j}/{len(v)}) 已下载：{real_url}")
    else:
        for city,areas in v.items():
            j += 1
            m =0
            weatherall[k][city] = {}
            for area,url in areas.items():
                m += 1
                if url == "javascript:void(0);":
                    real_url = url
                else:
                    real_url =  "http://www.weather.com.cn/weather/"+url[-22:-13] +'.shtml#search'
                weatherall[k][city][area] = get_7day_data(real_url)

                print(f"{k}({i}/{len(data)})  {city}({j}/{len(v)})  {area}({m}/{len(areas)})已下载：{real_url}")

js = json.dumps(weatherall,ensure_ascii=False,indent=4)
with open('天气数据/weather_data.json','w',encoding='utf-8')as f:
    f.write(js)

