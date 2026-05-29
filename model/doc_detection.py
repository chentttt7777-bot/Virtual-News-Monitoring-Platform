import logging
from docx import Document
import re

from .pdf_detection import extract_text_from_pdf

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

# 设置日志模版
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 当处理中文文本时，按照标点进行断句
def sent_tokenize(input_string):
    sentences = re.split(r'(?<=[。！？；?!])', input_string)
    # 去掉空字符串
    return [sentence for sentence in sentences if sentence.strip()]


# 从 .docx 文件中提取文本
def extract_text_from_docx(filename):
    doc = Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    # 将段落列表合并为一个字符串
    return '\n'.join(full_text)


# 将提取的文本按段落分割
def extract_paragraphs_from_text(full_text, min_line_length):
    paragraphs = []
    buffer = ''
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


# 将段落按一定粒度切割
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


# 获取段落
def getParagraphs(filename, min_line_length):
    if filename.endswith('.docx'):
        full_text = extract_text_from_docx(filename)
    elif filename.endswith('.pdf'):
        # 如果是 PDF 文件，调用之前的 PDF 处理函数
        full_text = extract_text_from_pdf(filename, None, min_line_length)
    else:
        raise ValueError("Unsupported file format")

    paragraphs = extract_paragraphs_from_text(full_text, min_line_length)
    chunks = split_text(paragraphs, 300, 50)
    return chunks

