import streamlit as sl
import json
import random

def read_articles(file_name):
    data = json.load(file_name)
    return data

def replace(article, keys):
    for i in range(len(keys)):
        article = article.replace('{{' + str(i + 1) + '}}', keys[i])
    return article

if __name__ == "__main__":

    sl.title("填词游戏")
    sl.write("by Clever_Jimmy")

    uploaded_file = sl.file_uploader("选择一个文件", type='json')
    if uploaded_file is not None:
        # 给定 json 题库
        data = read_articles(uploaded_file)
        articles = data["articles"]
        options = [item["title"] for item in articles]
        options.insert(0, "随机")
        # for item in articles:
            # options.append(item["title"])

        choice = sl.selectbox("请选择一篇文章", options)
        if choice == "随机":
            # 随机选择一篇文章
            idx = random.randint(0, len(articles) - 1)
            title = articles[idx]["title"]
            article = articles[idx]["article"]
            hints = articles[idx]["hints"]
        else:
            # 已指定文章
            for item in articles:
                if item["title"] == choice:
                    title = item["title"]
                    article = item["article"]
                    hints = item["hints"]

        sl.subheader(title)

        # 给出合适的输出，提示用户输入
        blanks = []
        for i in range(len(hints)):
            blanks.append(sl.text_input("第" + str(i + 1) + "空", key="blank" + str(i + 1), placeholder=hints[i]))

        confirm_button = sl.button("确认:white_check_mark:")
        if confirm_button:
            # 对文章进行替换
            result = replace(article, blanks)
            # 给出结果
            sl.write(result)
            # 提供文章的下载服务
            dwload_button = sl.download_button("下载本篇文章", data=result, file_name=title + ".txt")