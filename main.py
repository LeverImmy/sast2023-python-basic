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

    sl.set_page_config(
        page_title="填词游戏 - Clever_Jimmy",
        page_icon=":thinking_face:",
        layout="centered",
        initial_sidebar_state="auto",
        )

    sl.title("填词游戏")
    sl.write("by Clever_Jimmy")
    sl.write('''
            你需要上传题库并根据提示填空，然后就能欣赏自己的杰作啦！
             ''')

    uploaded_file = sl.file_uploader("选择一个题库文件", type='json')
    if uploaded_file is not None:
        # 给定 json 题库
        data = read_articles(uploaded_file)
        try:
            articles = data["articles"]
            options = [item["title"] for item in articles]
            options.insert(0, "【随机选一篇】")
            # 选择文章
            choice = sl.selectbox("请选择一篇文章", options)
            if choice == "【随机选一篇】":
                # 随机选择一篇文章
                if 'idx' not in sl.session_state:
                    sl.session_state['idx'] = random.randint(0, len(articles) - 1)
                idx = sl.session_state['idx']
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
            
            # 给出合适的输出，提示用户输入
            sl.divider()
            sl.subheader(title)
            blanks = []
            for i in range(len(hints)):
                blanks.append(sl.text_input("第" + str(i + 1) + "空", key="blank" + str(i + 1), placeholder=hints[i]))
            
            col1, col2 = sl.columns(2)
            with col1:
                confirm_button = sl.button("填好啦:white_check_mark:")
            with col2:
                reset_button = sl.button("再来一篇", type='primary')
            
            if confirm_button:
                # 先检查是不是每个空都填了
                all_finished = True
                for blank in blanks:
                    if not blank:
                        all_finished = False
                if all_finished:
                    # 对文章进行替换
                    result = replace(article, blanks)
                    # 给出结果
                    sl.divider()
                    sl.write("你填写的文章为：")
                    sl.write(result)
                    # 提供文章的下载服务
                    dwload_button = sl.download_button("下载本篇文章", data=result, file_name=title + ".txt")
                else:
                    # 给出未完成的警告
                    sl.warning("你还有未完成的空！", icon="⚠️")
            if reset_button:
                sl.session_state['idx'] = random.randint(0, len(articles) - 1)
        except:
            # 给出上传题库文件格式错误的警告
            sl.error("上传题库文件格式错误！", icon="🚨")