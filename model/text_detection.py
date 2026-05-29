# 导入相关库
import logging
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re

# 设置日志模版
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 当处理中文文本时，按照标点进行断句
def sent_tokenize(input_string):
    sentences = re.split(r'(?<=[。！？；?!])', input_string)
    # 去掉空字符串
    return [sentence for sentence in sentences if sentence.strip()]


# 将PDF文档处理函数得到的文本列表再按一定粒度，部分重叠式的切割文本，使上下文更完整
# chunk_size：每个文本块的目标大小（以字符为单位），默认为 200
# overlap_size：块之间的重叠大小（以字符为单位），默认为 100
def split_text(paragraphs, chunk_size=300, overlap_size=50):
    # 按指定 chunk_size 和 overlap_size 交叠割文本
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
    # logger.info(f"chunks: {chunks[0:10]}")
    return chunks


def process_text(text, min_line_length=1, chunk_size=300, overlap_size=50):
    # 将文本按行分割
    lines = text.split('\n')
    paragraphs = []
    buffer = ''

    # 将文本组织成段落
    for line in lines:
        if len(line) >= min_line_length:
            buffer += (' ' + line) if not line.endswith('-') else line.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)

    # 将段落分块
    chunks = split_text(paragraphs, chunk_size, overlap_size)
    return chunks
