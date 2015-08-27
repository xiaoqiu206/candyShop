# coding=utf-8
'''
Created on 2015年8月14日

@author: Administrator
'''
url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
post_data = {
    'cityName': '青岛',
    'StartTime': '2015-08-14',
    'DepTime': '2015-08-15',
    'operationtype': "NEWHOTELORDER",
    'IsOnlyAirHotel': "F",
    'cityId': "7",
    'cityPY': "qingdao",
    'cityCode': "0532",
    'htlPageView': "0",
    'hotelType': "F",
    'hasPKGHotel': "F",
    'requestTravelMoney': "F",
    'isusergiftcard': "F",
    'useFG': "F",
    'priceRange': "-2",
    'promotion': "F",
    'prepay': "F",
    'IsCanReserve': "F",
    'OrderBy': "99",
    'checkIn': "2015-08-14",
    'checkOut': "2015-08-15",
    'hidTestLat': "0%7C0",
    'AllHotelIds': "437482%2C535990%2C1483942%2C1371782%2C445195%2C1371788%2C1483944%2C1420488%2C996027%2C449574%2C436549%2C2045932%2C444953%2C371188%2C2004060%2C1179837%2C448693%2C1426280%2C689242%2C428042%2C1316453%2C1316341%2C480467%2C1316372%2C1502494",
    'psid': "h5%7C544%2Ch41%7C536%2Ch4%7C524%2Ch34%7C559%2Ch57%7C530",
    'HideIsNoneLogin': "T",
    'isfromlist': "T",
    'ubt_price_key': "htl_search_result_promotion",
    'showwindow': "2GybxYAM%2BEBp3vuwmGdSsQHaP7VOWMXfSh2XxvZXWJIytA2qIsCOFm8klN90dl5FSO1eOKV2qXLOXFr4J9Bid7vPQ7oa7aM%2BF%2Bp4hoIvWXvZSG59UCAqeeK8%2FNU03Y0ZdHY3VxT%2B1F0hNgTiUnDMQsAzae9n4Ye6DZ1TPygVmnlEQK8axuTzX16lzADeft6B%2F61RcBokE45w%2F1JJi7c5IFjBGfXC2HOHNtJnLFgTWfR3Zu%2Ff15BAJzq37ZTQbxuiPwaLVMrmCD47ZM72XwTsmVHos63LXddf3fvahgBa5e%2F4WzSc8juGME%2FqBKgJgZ576dZZkxjgU5K6wdeqM95DrojQbgoxXLOtDCqFpRfBs9BcAgS8uerm3hcZbn7EdXrzLmCZSM3MT74C8ml5f3cdnriySLMlbZy8chgjHmV%2FRU1sQOSi7Ohz%2BNo9K1ord7RTUKqHaua%2B8uEbv2xOpxK1IdB9AgdPXXvGvpjQ4l09dmbmnx%2FGkU46Vx4XtMepmiLNo6Xl0SF0mMN3BuQiO6p7yzqQtSlic0%2F8Ip9o7CUFJURIGAXvT1mjockfdJS679%2BLe3HqsqXJZmcSZbVgnAiHgu7clU%2BC0aKhJnAy%2Bhp5kQ1M2svg8Ww0jqLZl6EpPu3BEbrdq%2FIqrqsvat5Iz9YEFCwFCvcE5n0bjHEPu8kwmUKnmWBkQpQSXWfxwr2ZRDuNk7OYm80Y8C9uYyRceEvjfPHeTmvZ%2BWnLcD2Sw%2BhO%2BmKrfJisQnkQYIRt%2BQ%2FNKqByMqQfhp92A1ZOCgj%2BEHamEPDTxVrwJ5R8603jWC0%2BDRSDrRLRYZi%2FiRMSUhXMXn84Ght68Sl86xSbTtKDP6y4QP7nRc5SA1R5dg4uXRRoFOqkujJplRrKoA%3D%3D",
    'hotelIds': "437482_1_1,535990_2_1,1483942_3_1,1371782_4_1,445195_5_1,1371788_6_1,1483944_7_1,1420488_8_1,996027_9_1,449574_10_1,436549_11_1,2045932_12_1,444953_13_1,371188_14_1,2004060_15_1,1179837_16_1,448693_17_1,1426280_18_1,689242_19_1,428042_20_1,1316453_21_1,1316341_22_1,480467_23_1,1316372_24_1,1502494_25_1",
    'markType': "0",
    'a': "0",
    'price': "v0v149",
    'page': "1",
    'attachDistance': "0",
    'contyped': "0",
}
import urllib
import urllib2
response = urllib2.urlopen(url, urllib.urlencode(post_data))
print response.read()