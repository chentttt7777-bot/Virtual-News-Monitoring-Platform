import pandas as pd
import numpy as np
import chardet

# 检测文件编码

file_path = r'C:\PycharmProjects\CreativeProject\fake_news_detection_fyn20250220\data\A21_public_news.csv'
def getParagraphs(filename):
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())

    # 使用检测到的编码格式读取文件
    df = pd.read_csv(filename, encoding=result['encoding'])

    paragraphs = []

    df['total_content'] = ''

    for index, row in df.iterrows():
        title = row['title']
        content = row['content']
        if pd.notna(title) and pd.isna(content):
            df.at[index, 'total_content'] = title
        elif pd.isna(title) and pd.notna(content):
            df.at[index, 'total_content'] = content
        elif pd.notna(title) and pd.notna(content):
            df.at[index, 'total_content'] = f'{title}。{content}'

        paragraphs[index] = df.at[index, 'total_content']
    return paragraphs