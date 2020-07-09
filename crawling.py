import requests as r

import json

http_header = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                'x-requested-with': 'XMLHttpRequest'
                }

session = r.Session()

session.headers.update(http_header)

start = "서울시"

end = "남양주시"

search_distance_url_base = 'https://m.map.naver.com/spirra/findCarRoute.nhn?route=route3&output=json&result=web3&coord_type=latlng&search=2&car=0&mileage=12.4'

def SEARCH_DISTANCE_URL(start_point, end_point):
    return search_distance_url_base+'&start={}&destination={}'.format(start_point, end_point)
        
def SEARCH_POINT_URL(q):
    return 'https://m.map.naver.com/apis/search/poi?query={}&page=1'.format(q)
            
def GET_END_POINT(q):            
    res = session.get(SEARCH_POINT_URL(q)).text
    res_dict = json.loads(res)
    x = res_dict['result']['address']['list'][0]['x']
    y = res_dict['result']['address']['list'][0]['y']
    name = res_dict['result']['address']['list'][0]['name']
    return '{},{},{}'.format(x, y, name)
                                                                            
def GET_INFO(start, end):
    start_point = GET_END_POINT(start)
    end_point = GET_END_POINT(end)
    
    res = session.get(SEARCH_DISTANCE_URL(start_point, end_point)).text
    res_dict = json.loads(res)
    
    target = res_dict['routes'][0]['summary']
    distance = target['distance']
    sec = target['duration']
    taxi_fare = target['taxi_fare']
    print('검색완료')
    print('출발지: {}, 도착지: {}'.format(start, end))
    print('추천경로 이동 거리: {}km'.format(distance/1000))
    print('예상 소요시간: {}분'.format(sec/60))
    print('예상 택시요금: {}원'.format(taxi_fare))

GET_INFO(start, end)
