#coding:utf-8
import json
import codecs
class StackJsonPipeline:

    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('crawled/score_netease.json', 'w', encoding='utf-8')

    # 存储数据，将 Item 实例作为 json 数据写入到文件中
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item
    # 处理结束后关闭 文件 IO 流
    def close_spider(self, spider):
        self.file.close()