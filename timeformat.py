"""
%y 两位数的年份表示�?00-99�?
%Y 四位数的年份表示�?000-9999�?
%m 月份�?01-12�?
%d 月内中的�?天（0-31�?
%H 24小时制小时数�?0-23�?
%I 12小时制小时数�?01-12�?
%M 分钟数（00=59�?
%S 秒（00-59�?
%a 本地�?化星期名�?
%A 本地完整星期名称
%b 本地�?化的月份名称
%B 本地完整的月份名�?
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366�?
%p 本地A.M.或P.M.的等价符
%U �?年中的星期数�?00-53）星期天为星期的�?�?
%w 星期�?0-6），星期天为星期的开�?
%W �?年中的星期数�?00-53）星期一为星期的�?�?
%x 本地相应的日期表�?
%X 本地相应的时间表�?
%Z 当前时区的名�?
%% %号本�?
"""

from _datetime import datetime
import time


print(time.time())
print(time.localtime())
print(time.strftime("%Y-%m-%d"))
# print(datetime.date("20180808"))
# ntime = time.struct_time(tm_year=2010, tm_mon=7, tm_mday=19, tm_hour=22, tm_min=33, tm_sec=39, tm_wday=0, tm_yday=200, tm_isdst=0)
print(time.strftime("%Y-%m-%d",time.localtime(1120180808)))
