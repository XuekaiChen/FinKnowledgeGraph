import tushare as ts
import pandas as pd

# 和 Tushare 建立连接
pro = ts.pro_api('08fbab8087eb66409ec66452b756beb05ef93388bbba7905fab1f7b5')

# 股票基本信息
# 查询当前所有正常上市交易的股票列表
# https://waditu.com/document/2?doc_id=25
# 可以限制exchange='SSE'表示上交所
# list_status='L'表示上市公司
# ts_code: TS代码
# symbol: 股票代码
# name: 股票名称
# area：地域
# industry: 行业
stock_basic = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name,area,industry,fullname')
stock_basic.to_csv('./data/knowledge/股票信息1.csv', encoding='gbk')

# 概念股分类 https://waditu.com/document/2?doc_id=125
concept = pro.concept()
concept.to_csv('./data/knowledge/概念信息1.csv', encoding='gbk', index=False)

# # 股票概念信息，获取概念下对应的股票（概念信息.csv 文件中共有 358 个 概念）
# concept_details = pd.DataFrame(columns=('id', 'concept_name', 'code', 'name'))
#
# for i in range(359):
#     concept_id = 'TS' + str(i)
#     # 获取该概念下的全部股票 https://waditu.com/document/2?doc_id=126
#     concept_stocks = pro.concept_detail(id=concept_id, field='concept_name,code,name')
#     concept_details = concept_details.append(concept_stocks)
# concept_details.to_csv('./data/knowledge/股票-概念信息1.csv', encoding='gbk')
#
#
# # 股票持有股东信息
# holder_basic = []
# # TS代码、公告日期、报告期、股东名、持有量、持有占比
# stock_holders = pd.DataFrame(columns=('ts_code', 'ann_date', 'end_date', 'holder_name', 'hold_amount', 'hold_ratio'))
# # 获取时间段内股票的股东信息
# for each_code in stock_basic['ts_code'].tolist():
#     # 前十大股东：https://waditu.com/document/2?doc_id=61
#     curr_holder = pro.top10_holders(ts_code=each_code, start_date='20200101', end_date='20201231')
#     # 在这里，简单起见，只考虑第一个股东信息
#     stock_holders = stock_holders.append(curr_holder.iloc[0:1])
#     # 加入股东名称
#     # 加入时做清洗，即去除 -，比如将 新华人寿保险股份有限公司-分红-个人分红-018L-FH002深 清洗为 新华人寿保险股份有限公司
#     holder_basic.extend(curr_holder.iloc[0:1]['holder_name'].values.tolist().split('-')[0])
# stock_holders.to_csv('./data/knowledge/股票-股东信息.csv', encoding='gbk')
#
# # 股东信息
# holder_basic_df = pd.DataFrame({
#     '股东名称': list(set(holder_basic))
# })
# holder_basic_df.to_csv('./data/knowledge/股东信息.csv', encoding='gbk', index=False)

