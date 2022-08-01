from pyspark.sql import SparkSession

sc = SparkSession.builder.appName('udf_home_task').enableHiveSupport().getOrCreate()

def stop_spark_app():
    """Stop spark applcation"""
    sc.stop()

columns = ["id", "stock_prices"]
data = [("1", [10, 7, 5, 8, 11, 9])]
df = sc.createDataFrame(data, columns)
df.createTempView("temp")

def get_max_profit(stock_prices):
    """Полчение максимальной прибыль от одной сделки с одной акцией"""
    if len(stock_prices) < 2:
        raise IndexError('Прибыль отстутствует, так как колчества цен в массиве меньше двух')
    min_price = stock_prices[0]
    max_profit = stock_prices[1] - stock_prices[0]

    for index, price in enumerate(stock_prices):
        if index == 0:
            continue
        potential_profit = price - min_price
        max_profit = max_profit if max_profit > potential_profit else potential_profit
        min_price  = min_price if min_price < price else price
    return max_profit

stock_prices_yesterday = [10, 7, 5, 8, 11, 9]

profit = get_max_profit(stock_prices_yesterday)
sc.udf.register("get_max_profit", get_max_profit)
sc.sql("select * from temp").show()
sc.sql("select id, stock_prices, get_max_profit(stock_prices) from temp").show()
stop_spark_app()

