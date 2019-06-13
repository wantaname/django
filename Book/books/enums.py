'''
书籍类别
'''
PYTHON = 1
JAVASCRIPT = 2
ALGORITHMS = 3
MACHINELEARNING = 4
OPERATINGSYSTEM = 5
DATABASE = 6
OTHER=7

BOOKS_TYPE = {
    PYTHON: '后端开发',
    JAVASCRIPT: '前端开发',
    ALGORITHMS: '数据结构&算法',
    MACHINELEARNING: '人工智能&大数据',
    OPERATINGSYSTEM: '网络&操作系统',
    DATABASE: '数据库',
    OTHER:'其他',
}

OFFLINE = 0
ONLINE = 1

STATUS_CHOICE = {
    OFFLINE: '下线',
    ONLINE: '上线'
}
