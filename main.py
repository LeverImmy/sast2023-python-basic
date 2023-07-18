import argparse
import json
import random

def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -f 为必选参数，表示输入题库文件
    2. -ch 为可选参数，表示是否指定文章
    ...

    :return: 参数
    """
    parser = argparse.ArgumentParser(
        prog="Word filling game",
        description="A simple game",
        allow_abbrev=True
    )

    parser.add_argument("-f", "--file", help="题库文件", required=True)
    # TODO: 添加更多参数
    parser.add_argument("-ch", "--choose", help="是否指定文章", required=False)
    
    args = parser.parse_args()
    return args



def read_articles(filename):
    """
    读取题库文件

    :param filename: 题库文件名

    :return: 一个字典，题库内容
    """
    with open(filename, 'r', encoding="utf-8") as f:
        # TODO: 用 json 解析文件 f 里面的内容，存储到 data 中
        data=json.load(f)
    
    return data



def get_inputs(hints):
    """
    获取用户输入

    :param hints: 提示信息

    :return: 用户输入的单词
    """

    keys = []
    for hint in hints:
        print(f"请输入{hint}：")
        # TODO: 读取一个用户输入并且存储到 keys 当中
        keys.append(input().strip())

    return keys


def replace(article, keys):
    """
    替换文章内容

    :param article: 文章内容
    :param keys: 用户输入的单词

    :return: 替换后的文章内容

    """
    for i in range(len(keys)):
        # TODO: 将 article 中的 {{i}} 替换为 keys[i]
        # hint: 你可以用 str.replace() 函数，也可以尝试学习 re 库，用正则表达式替换
        article=article.replace('{{' + str(i + 1) + '}}', keys[i])

    return article


if __name__ == "__main__":
    args = parser_data()
    data = read_articles(args.file)
    articles = data["articles"]

    # TODO: 根据参数或随机从 articles 中选择一篇文章
    choose = args.choose
    if choose:
        # 已指定文章
        for item in articles:
            if item["title"] == choose:
                title = item["title"]
                article = item["article"]
                hints = item["hints"]
    else:
        # 随机选择文章
        idx = random.randint(0, len(articles))
        title = articles[idx]["title"]
        article = articles[idx]["article"]
        hints = articles[idx]["hints"]

    user_keys = []
    
    # TODO: 给出合适的输出，提示用户输入
    user_keys = get_inputs(hints)

    # TODO: 获取用户输入并进行替换
    result = replace(article, user_keys)

    # TODO: 给出结果
    print(title + '\n' + result)
