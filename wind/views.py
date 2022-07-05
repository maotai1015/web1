from django.http import JsonResponse
from wind.models import KLine, DayData
# Create your views here.
from django.views import View
# OK
# 数据处理类




# 测试2.0


class Result:
    def __init__(self,data):
        self.status = 0
        self.msg = ""
        self. data = data

    # 时间日期格式转换
    def datetimeformat(self, original_date, original_time):
        # 时间
        time_list = list(str(original_time))
        format_time = ''.join(time_list)
        if len(format_time) < 4:
            format_time = "0" + format_time
        # 日期
        date_list = list(str(original_date))
        date_list.insert(4, "-")
        date_list.insert(7, "-")
        format_date = ''.join(date_list)
        return format_date,format_time

    # 主页
    def toindex(self):
        for i in self.data:
            i["pricePreviousday"] = i["pricePreviousday"] / 10000
            i["priceOpening"] = i["priceOpening"] / 10000
            i["priceHigh"] = i["priceHigh"] / 10000
            i["priceLow"] = i["priceLow"] / 10000
            i["priceNow"] = i["priceNow"] / 10000
            i["priceSell"] = i["priceSell"] / 10000
            i["priceBuy"] = i["priceBuy"] / 10000
            i["transactionDay"], i["transactionTime"] = self.datetimeformat(i["transactionDay"], i["transactionTime"]//100000)
        data_sort = sorted(self.data, key=lambda keys: keys["stockNum"])
        return {'status': self.status, 'msg': self.msg, "data": data_sort}

    # K线获取
    def tokline(self):
        try:
            for i in range(len(self.data)):
                self.data[i]["pricePreviousday"] = self.data[i]["pricePreviousday"]/10000
                self.data[i]["priceOpening"] = self.data[i]["priceOpening"]/10000
                self.data[i]["priceHigh"] = self.data[i]["priceHigh"]/10000
                self.data[i]["priceLow"] = self.data[i]["priceLow"]/10000
                self.data[i]["priceNow"] = self.data[i]["priceNow"]/10000
                self.data[i]["priceSell"] = self.data[i]["priceSell"]
                self.data[i]["priceBuy"] = self.data[i]["priceBuy"]
                self.data[i]["transactionDay"], self.data[i]["transactionTime"] = self.datetimeformat(self.data[i]["transactionDay"],
                                                                                self.data[i]["transactionTime"] // 100000)

                # 5日均线计算
                sum = 0
                if i >= 5:
                    for j in range(i-5, i):
                        sum += self.data[j]['priceNow']
                    self.data[i]["fiveAvg"] = round(sum/5, 2)    # 结果保留两位小数
                else:
                    for j in range(0, i+1):
                        sum += self.data[j]['priceNow']
                    self.data[i]["fiveAvg"] = round(sum/(i+1), 2)     # 结果保留两位小数
            self.status = 0
            self.msg = "success"
        except:
            self.status = 1
            self.msg = ""
        return {'status': self.status, 'msg': self.msg, "data": self.data}

    # 单只走势图
    def totrend(self):
        try:
            dataresult = []  # 数据处理结果列表
            pricePreviousday = self.data[0]['pricePreviousday'] / 10000  # 记录前日收盘价
            turnover = self.data[0]['transactionNumtotal']  # 每分钟成交量   # 首先记录第一条
            timemark = self.data[0]['transactionTime'] // 100000  # 开始时间标记    格式0846
            data_last = self.data[-1]  # 最后一条数据
            '''
             成交量说明：
                以分钟为界限，收到数据的时间跨越分钟的话，按前一分钟的内成交量计算
                判断时间相等  
            '''
            datalen = len(self.data)
            for i in range(1, datalen):
                time_current = self.data[i]['transactionTime']//100000  # 当前数据时间
                if time_current == timemark:
                    turnover += (self.data[i]['transactionNumtotal'] - self.data[i-1]['transactionNumtotal'])
                else:

                    '''
                    保存上一分钟成交量等数据
                    '''
                    dataMinute = {}
                    dataMinute['pricePreviousday'] = pricePreviousday    #  前日收盘价
                    dataMinute['priceNow'] = self.data[i-1]['priceNow'] / 10000  # 一分钟内最后一条数据的价格
                    dataMinute["transactionDay"], dataMinute["transactionTime"] = self.datetimeformat(self.data[i]["transactionDay"], timemark)  # 时间格式转换
                    dataMinute["turnover"] = turnover    # 成交量
                    dataresult.append(dataMinute)

                    turnover = 0  # 下一分钟开始  成交量归0
                    timemark = time_current    # 时间标记更新
                if i == datalen -1 :
                    dataMinute = {}
                    dataMinute['pricePreviousday'] = pricePreviousday  # 前日收盘价
                    dataMinute['priceNow'] = self.data[i]['priceNow'] / 10000  # 当前价
                    dataMinute["transactionDay"], dataMinute["transactionTime"] = self.datetimeformat(self.data[i]["transactionDay"], timemark)  # 时间格式转换
                    dataMinute["turnover"] = turnover  # 成交量
                    dataresult.append(dataMinute)

            self.status = 0
            self.msg = "success"
        except:
            dataresult = ""
            self.status = 1
            self.msg = ""
        return {'status': self.status, 'msg': self.msg, "data": dataresult}

class Index(View):

    def get(self, request):
        kLine = KLine.objects.all().order_by("-transactionDay").values()[:50]
        result = Result(list(kLine)).toindex()
        return JsonResponse(result)


class Kline(View):
    def get(self, request):
        stock = request.GET.get("num", " ")
        dataQuery = KLine.objects.filter(stockNum=stock).values()
        result = Result(list(dataQuery)).tokline()
        return JsonResponse(result)

class Trend(View):
    def get(self, request):
        stock = request.GET.get("num", " ")
        dataQuery = DayData.objects.filter(stockNum=stock).values()
        result = Result(list(dataQuery)).totrend()
        return JsonResponse(result)

# def index(request):
#     dataQuery = DayData.objects.all().order_by("-transactionTime").distinct()[:100]
#     print(dataQuery)
#     kLine = KLine.objects.all().order_by("-transactionDay").values()[:50]
#     result = Result(list(kLine)).toindex()
#     return JsonResponse(result)


# def kline(request):
#     if request.method == "GET":
#         stock = request.GET.get("num", " ")
#         dataQuery = KLine.objects.filter(stockNum=stock).values()
#         result = Result(list(dataQuery)).tokline()
#         return JsonResponse(result)

#
# def trend(request):
#     if request.method == "GET":
#         stock = request.GET.get("num", " ")
#         dataQuery = DayData.objects.filter(stockNum=stock).values()
#         result = Result(list(dataQuery)).totrend()
#         return JsonResponse(result)
