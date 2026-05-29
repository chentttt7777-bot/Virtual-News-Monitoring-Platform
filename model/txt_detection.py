import logging
import re


# 设置日志模板
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 当处理中文文本时，按照标点进行断句
def sent_tokenize(input_string):
    sentences = re.split(r'(?<=[。！？；?!])', input_string)
    # 去掉空字符串
    return [sentence for sentence in sentences if sentence.strip()]


# 从TXT文件中提取文本
def extract_text_from_txt(filename, min_line_length):
    paragraphs = []
    buffer = ''

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for text in lines:
        text = text.strip()
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''

    if buffer:
        paragraphs.append(buffer)

    return paragraphs


# 将文本列表再按一定粒度，部分重叠式的切割文本，使上下文更完整
def split_text(paragraphs, chunk_size=300, overlap_size=50):
    sentences = [s.strip() for p in paragraphs for s in sent_tokenize(p)]
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = sentences[i]
        overlap = ''
        prev_len = 0
        prev = i - 1
        # 向前计算重叠部分
        while prev >= 0 and len(sentences[prev]) + len(overlap) <= overlap_size:
            overlap = sentences[prev] + ' ' + overlap
            prev -= 1
        chunk = overlap + chunk
        next = i + 1
        # 向后计算当前chunk
        while next < len(sentences) and len(sentences[next]) + len(chunk) <= chunk_size:
            chunk = chunk + ' ' + sentences[next]
            next += 1
        chunks.append(chunk)
        i = next
    return chunks


def getParagraphs(filename, min_line_length):
    paragraphs = extract_text_from_txt(filename, min_line_length)
    chunks = split_text(paragraphs, 300, 50)
    return chunks

