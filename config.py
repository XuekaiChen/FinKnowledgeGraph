# 知识语料路径
entity_corpus_path = '../data/knowledge/'

# 实体搜索器存储路径
entity_searcher_save_path = '../checkpoints/entity_searcher/search_tree.pkl'

# 实体搜索器加载路径
entity_searcher_load_path = './checkpoints/entity_searcher/search_tree.pkl'

# 分类器语料路径
classifier_corpus_path = '../data/classifier/chat.train'

# 分类器模型存储路径
classifier_save_path = '../checkpoints/classifier/model.bin'

# 分类器模型加载路径
classifier_load_path = './checkpoints/classifier/model.bin'

# 闲聊回复语料库
chat_responses = {
    'qa': [],
    'greet': [
        'hello，我是小A，小哥哥小姐姐有关于股票的问题可以问我哦',
        '你好，我是小A，输入股票名称或者代码查看详细信息哦',
        '你好，我是小A，可以问我股票相关的问题哦'
    ],
    'goodbye': [
        '再见',
        '不要走，继续聊会呗',
        '拜拜喽，别忘了给个小红心啊',
    ],
    'bot': [
        '没错，我就是集美貌与才智于一身的小A',
        '小A就是我，我就是小A'
    ],
    'safe': [
        '不好意思，您的问题我没太听懂，可以换一种说法嘛',
        '亲亲，这里好像没有您想要的答案'
    ]
}

# 问题类型
question_types = {
    'concept':
        ['概念', '特征'],
    'holder':
        ['股东', '控制', '控股', '持有'],
    'industry':
        ['行业', '领域'],
}

# 存储对话历史中上一次涉及的问题类型和实体
contexts = {
    'ques_types': None,
    'entities': None
}
