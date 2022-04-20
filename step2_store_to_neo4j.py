from tqdm import tqdm
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher

# --------------------------- 连接 Neo4j
# 官方文档：https://py2neo.org/2021.1/
graph = Graph('http://localhost:7474/finance_demo/db/', auth=('neo4j', 'neo4j123'))
print(graph)
graph.run('match (n) detach delete n')# 删除所有节点及其关系
# --------------------------- 创建实体
# 股票
print('创建 股票 实体...')
stock_basic = pd.read_csv('./data/knowledge/股票信息.csv', encoding='gbk')
for idx, each_row in tqdm(stock_basic.iterrows()):
    # 方法说明：https://py2neo.org/2021.1/data/index.html#py2neo.data.Node
    # 股票 是 label
    # keyword arguments 是属性，如 TS代码 等
    each_stock = Node('股票',
                      TS代码=each_row['ts_code'],
                      股票代码=each_row['symbol'],
                      股票名称=each_row['name'],
                      行业=each_row['industry'])
    try:
        # 方法说明：https://py2neo.org/2021.1/workflow.html#py2neo.Transaction.create
        graph.create(each_stock)
    except Exception as e:
        print(f'Error: {e}, data idx: {idx}, data: {each_row}')

# 概念
print('创建 概念 实体...')
concept = pd.read_csv('./data/knowledge/概念信息.csv', encoding='gbk')
for idx, each_row in tqdm(concept.iterrows()):
    each_concept = Node('概念',
                        概念代码=each_row['code'],
                        概念名称=each_row['name'])
    graph.create(each_concept)

# 股东
print('创建 股东 实体...')
holder = pd.read_csv('./data/knowledge/股东信息.csv', encoding='gbk')
for idx, each_row in tqdm(holder.iterrows()):
    each_holder = Node('股东',
                       股东名称=each_row['name'])
    graph.create(each_holder)

# # --------------------------- 创建关系
# # 方法说明：https://py2neo.org/2021.1/matching.html#py2neo.NodeMatcher
# matcher = NodeMatcher(graph)
#
# # 股票-概念
# print('创建 股票-概念 关系...')
# stock_concept = pd.read_csv('./data/knowledge/股票-概念信息.csv', encoding='gbk')
# for idx, each_row in tqdm(stock_concept.iterrows()):
#     node1 = matcher.match("股票", TS代码=each_row['ts_code']).first()
#     node2 = matcher.match("概念", 概念代码=each_row['Cid']).first()
#     # node1 = graph.nodes.match("股票", TS代码=each_row['ts_code']).first()
#     # node2 = graph.nodes.match("概念", 概念代码=each_row['Cid']).first()
#
#     if node1 is not None and node2 is not None:
#         # 方法说明：https://py2neo.org/2021.1/data/index.html#py2neo.data.Relationship
#         # 格式：Relationship(start_node, type, end_node)
#         r = Relationship(node1, '所属概念', node2)
#         graph.create(r)
#
#
# # 股票-股东
# print('创建 股票-股东 关系...')
# stock_holder = pd.read_csv('./data/knowledge/股票-股东信息.csv', encoding='gbk')
# for idx, each_row in tqdm(stock_holder.iterrows()):
#     # first() 方法返回第一个匹配的 Node，如果找不到则返回 None
#     node1 = graph.nodes.match("股票", TS代码=each_row['ts_code']).first()
#     node2 = graph.nodes.match("股东", 股东名称=each_row['holder_name'].split('-')[0]).first()  # 取最前面的子公司
#     if node1 is not None and node2 is not None:
#         r = Relationship(node2, '持有', node1,
#                          ann_date=each_row['ann_date'],
#                          end_date=each_row['end_date'],
#                          hold_amount=each_row['hold_amount'],
#                          hold_ratio=each_row['hold_ratio'])
#         graph.create(r)

#-----------------上面创建关系的方式由于py2neo版本问题总报错，因此改为用cypher语句导入关系
# 创建所属关系
print('创建 股票-概念 关系...')
stock_concept = pd.read_csv('./data/knowledge/股票-概念信息.csv', encoding='gbk')
for idx, each_row in tqdm(stock_concept.iterrows()):
    cypher_sql = "MATCH (a:`股票`),(b:`概念`) WHERE a.`TS代码` = '{0}' AND b.`概念代码` = '{1}'" \
                 " CREATE (a)-[r:所属概念] -> (b) RETURN r"\
                 .format(str(each_row['ts_code']),str(each_row['Cid']))
    graph.run(cypher_sql)

# 创建持有关系
print('创建 股票-股东 关系...')
stock_concept = pd.read_csv('./data/knowledge/股票-股东信息.csv', encoding='gbk')
for idx, each_row in tqdm(stock_concept.iterrows()):
    cypher_sql = "MATCH (a:`股东`),(b:`股票`) WHERE a.`股东名称` = '{0}' AND b.`TS代码` = '{1}' " \
                 "CREATE (a)-[r:持有{{公告日期:'{2}', 报告期:'{3}', 持有量:'{4}', 占比:'{5}'}}] -> (b)"\
                 .format(str(each_row['holder_name'].split('-')[0]), str(each_row['ts_code']),
                         str(each_row['ann_date']), str(each_row['end_date']),
                         str(each_row['hold_amount']), str(each_row['hold_ratio']))
    graph.run(cypher_sql)


print('实体 关系 导入成功...')
