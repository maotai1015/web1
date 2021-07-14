from django.db import models

# Create your models here.


from django.db import models
# Create your models here.


class StockData(models.Model):
    stockNum = models.CharField(max_length=50, verbose_name="股票代码")
    stockName = models.CharField(max_length=50, verbose_name="股票名称")

    class Meta:
        db_table = "stockdata"               # 表名
        verbose_name = "股票名称"              # 后台显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return "标号：%s--股票：%s" % (self.stockNum, self.stockName)


class KLine(models.Model):
    stockNum = models.CharField(max_length=15, verbose_name="股票代码", db_index=True)      # 建立索引
    transactionDay = models.CharField(max_length=15, verbose_name="交易日")
    transactionTime = models.IntegerField(verbose_name="交易时间")
    pricePreviousday = models.FloatField(verbose_name="前日收盘价")
    priceOpening = models.FloatField(verbose_name="开盘价")
    priceHigh = models.FloatField(verbose_name="最高价")
    priceLow = models.FloatField(verbose_name="最低价")
    priceNow = models.FloatField(verbose_name="当前价")
    priceSell = models.FloatField(verbose_name="申卖价")
    sellAmount = models.FloatField(verbose_name="申卖量")
    priceBuy = models.FloatField(verbose_name="申买价")
    buyAmount = models.FloatField(verbose_name="申买量")
    transactionNum = models.FloatField(verbose_name="成交笔数")
    transactionNumtotal = models.FloatField(verbose_name="成交总量")
    transactionPricetotal = models.FloatField(verbose_name="成交总金额")


    class Meta:
        db_table = "kline"
        verbose_name = "历史K线"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "股票：%s--交易日：%s--交易时间：%s" % (self.stockNum, self.transactionDay, self.transactionTime)


class DayData(models.Model):
    stockNum = models.CharField(max_length=15, verbose_name="股票代码", db_index=True)
    transactionDay = models.CharField(max_length=15, verbose_name="交易日")
    transactionTime = models.IntegerField(verbose_name="交易时间")
    pricePreviousday = models.FloatField(verbose_name="前日收盘价")
    priceOpening = models.FloatField(verbose_name="开盘价")
    priceHigh = models.FloatField(verbose_name="最高价")
    priceLow = models.FloatField(verbose_name="最低价")
    priceNow = models.FloatField(verbose_name="当前价")
    priceSell = models.FloatField(verbose_name="申卖价", null=True)
    sellAmount = models.FloatField(verbose_name="申卖量", null=True)
    priceBuy = models.FloatField(verbose_name="申买价", null=True)
    buyAmount = models.FloatField(verbose_name="申买量", null=True)
    transactionNum = models.FloatField(verbose_name="成交笔数", null=True)
    transactionNumtotal = models.FloatField(verbose_name="成交总量")
    transactionPricetotal = models.FloatField(verbose_name="成交总金额")

    class Meta:
        db_table = "daydata"
        verbose_name = "当日数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "股票：%s--交易日：%s--交易时间：%s" % (self.stockNum, self.transactionDay, self.transactionTime)





