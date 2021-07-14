from django.test import TestCase

# Create your tests here.
import datetime
# import pymysql
# conn = pymysql.connect(host="127.0.0.1", user="root", password="141106", database="wind_web")
# cursor = conn.cursor()


# def savetomysql(data):
#     key = ", ".join('{}'.format(k) for k in data.keys())
#     values = ', '.join("'{}'".format(k) for k in data.values())
#     sql = r"insert into daydata(%s) values(%s)"
#     res_sql = sql % (key, values)
#     cursor.execute(res_sql, data)
#     conn.commit()
#
#
# d = {'stockNum': '603160.SH', 'transactionDay': '20210519', 'transactionTime': '1301', 'pricePreviousday': 116.0, 'priceHigh': 117.62, 'priceLow': 114.34, 'priceOpening': 115.29, 'priceNow': '1167600', 'transactionNumtotal': '2789332', 'transactionPricetotal': '323799045'}
# savetomysql(d)
# a = "20210201"
# b = "20210202"
# str_list = list(a)
# str_list.insert(4, "-")
# str_list.insert(7, "-")
# a_b = ''.join(str_list)
# print(a_b)

a = [1,2,3]
for i in range(0,len(a)):
    print(i)
print(len(a))