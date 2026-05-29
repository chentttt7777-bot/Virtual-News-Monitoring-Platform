from django.core.files.storage import default_storage
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import magic
import os
from model import pdf_detection
from model import text_detection
from model import doc_detection
from model import txt_detection
from model import link_detection
from model import bert_detection
from model import xlsx_detection
from model import roberta_detection
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from fpdf import FPDF
from model import generators
from model import exceptions
import random
from news_detector import settings
from django.http import FileResponse

ALLOWED_TYPES = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'text/plain': 'txt',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx'
}


def url_to_path(file_url):
    """将/media/开头的URL转换为服务器物理路径"""
    if file_url.startswith('/media/'):
        return os.path.join(settings.MEDIA_ROOT, file_url[7:])
    return file_url  # 如果不是/media/开头，按原路径处理


@api_view(['POST'])
def bert_file_analyze(request):
    file_url = request.data.get("filepath", "")
    filepath = url_to_path(file_url)
    file_type = os.path.splitext(filepath)[1][1:]

    if not filepath:
        return Response({"error": "未提供文件路径"}, status=400)

        # 2. 安全检查：防止路径遍历攻击
    if '../' in filepath or not os.path.exists(filepath):
        return Response({"error": "无效的文件路径"}, status=400)
    if file_type == 'pdf':
        paragraphs = pdf_detection.getParagraphs(
            filepath,
            # page_numbers=[2, 3], # 指定页面
            page_numbers=None,  # 加载全部页面
            min_line_length=1
        )
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = bert_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    elif file_type == 'doc' or file_type == 'docx':
        paragraphs = doc_detection.getParagraphs(
            filepath,
            min_line_length=1
        )
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = bert_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    elif file_type == 'txt':
        paragraphs = txt_detection.getParagraphs(
            filepath,
            min_line_length=1
        )
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = bert_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    elif file_type == 'xlsx':
        paragraphs = xlsx_detection.getParagraphs(filepath)
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = bert_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
        # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)


@api_view(['POST'])
def bert_content_analyze(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "没有提供文本"}, status=400)
    length_content = len(text)
    if length_content > 150:
        paragraphs = text_detection.process_text(text, min_line_length=1)
        length = len(paragraphs)
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = bert_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    else:
        ai_probability = bert_detection.predict(text)
        return Response({'content': text,
                         "probability": ai_probability[0] * 100})


@api_view(['POST'])
def bert_link_analyze(request):
    url = request.data.get("url", "")
    content = link_detection.get_news_content(url)
    if content:
        paragraphs = text_detection.process_text(content, min_line_length=1)
        length = len(paragraphs)
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = bert_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    else:
        return Response({"error": "无法获取链接内容"}, status=400)


@api_view(['POST'])
def roberta_file_analyze(request):
    file_url = request.data.get("filepath", "")
    filepath = url_to_path(file_url)
    file_type = os.path.splitext(filepath)[1][1:]
    if file_type == 'pdf':
        paragraphs = pdf_detection.getParagraphs(
            filepath,
            # page_numbers=[2, 3], # 指定页面
            page_numbers=None,  # 加载全部页面
            min_line_length=1
        )
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = roberta_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    elif file_type == 'doc' or file_type == 'docx':
        paragraphs = doc_detection.getParagraphs(
            filepath,
            min_line_length=1
        )
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = roberta_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    elif file_type == 'txt':
        paragraphs = txt_detection.getParagraphs(
            filepath,
            min_line_length=1
        )
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = roberta_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    elif file_type == 'xlsx':
        paragraphs = xlsx_detection.getParagraphs(filepath)
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = roberta_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
        # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)


@api_view(['POST'])
def roberta_content_analyze(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "没有提供文本"}, status=400)
    length_content = len(text)
    if length_content > 150:
        paragraphs = text_detection.process_text(text, min_line_length=1)
        length = len(paragraphs)
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = roberta_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    else:
        ai_probability = roberta_detection.predict(text)
        return Response({"content": text,
                         "probability": ai_probability[0] * 100})


@api_view(['POST'])
def roberta_link_analyze(request):
    url = request.data.get("url", "")
    content = link_detection.get_news_content(url)
    if content:
        paragraphs = text_detection.process_text(content, min_line_length=1)
        length = len(paragraphs)
        answer = {}
        length = len(paragraphs)
        for i in range(length):
            probability = roberta_detection.predict(paragraphs[i])
            answer[i] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
        result_array = list(answer.values())

        # 使用DRF的Response返回，会自动转换为JSON
        return Response(result_array)
    else:
        return Response({"error": "无法获取链接内容"}, status=400)


@require_http_methods(["POST"])
@ensure_csrf_cookie  # 确保返回CSRF cookie
def upload_file(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': '未检测到文件'}, status=400)

    try:
        file = request.FILES['file']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # 安全处理文件名
        file_name = default_storage.get_valid_name(file.name)
        file_path = default_storage.save(os.path.join('uploads', file_name), file)

        return JsonResponse({
            'filename': file_name,
            'filepath': os.path.join(settings.MEDIA_URL, file_path)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_random_filename():
    # 生成随机10位数字组成的文件名
    random_digits = ''.join(random.choices('0123456789', k=10))
    return f"{random_digits}.pdf"


class PDFWithBackground(FPDF):
    # 自定义PDF类，添加背景图片支持

    def header(self):
        # 设置背景图片
        self.image(os.path.join(os.path.dirname(__file__), "../static/images/bg_pdf.png"), 0, 0, self.w, self.h)


def save_to_pdf(data, filename, filepath):
    # 将分析结果保存为PDF
    if filename is None:
        # 如果未提供文件名，则生成随机文件名
        filename = generate_random_filename()

    pdf = PDFWithBackground()
    pdf.add_page()

    # 添加字体支持
    font_path = os.path.join(os.path.dirname(__file__), "../static/ttf/SimHei.ttf")
    pdf.add_font("SimHei", "", font_path, uni=True)
    font_path_English = os.path.join(os.path.dirname(__file__), "../static//ttf/Times New Roman.ttf")
    pdf.add_font("TimesNewRoman", "", font_path_English, uni=True)
    pdf.set_font("SimHei", size=12)

    # 标题
    pdf.set_text_color(40, 157, 255)
    pdf.set_font("SimHei", size=26)
    pdf.cell(200, 10, txt="事实核查报告", ln=1, align="C")
    pdf.ln(8)  # 减少标题后的间距

    # 概要
    pdf.set_text_color(40, 157, 255)
    pdf.set_font("SimHei", size=20)
    pdf.cell(200, 10, txt="概要", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("SimHei", size=14)
    pdf.multi_cell(0, 8, txt=data["summary"])  # 调整行高
    pdf.ln(4)  # 减少段后间距

    # 风险等级
    pdf.set_text_color(40, 157, 255)
    pdf.set_font("SimHei", size=20)
    pdf.cell(200, 10, txt="风险等级", ln=1)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font("TimesNewRoman", size=16)
    pdf.cell(0, 8, txt=data["risk_level"].upper(), ln=1)  # 调整行高
    pdf.ln(4)  # 减少段后间距

    # 核查证据
    pdf.set_text_color(40, 157, 255)
    pdf.set_font("SimHei", size=20)
    pdf.cell(200, 10, txt="核查证据", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("SimHei", size=14)
    for idx, evidence in enumerate(data["evidence"], 1):
        pdf.multi_cell(0, 8, txt=f"{idx}. {evidence}")  # 调整行高
    pdf.ln(4)  # 减少段后间距

    # 处理建议
    pdf.set_text_color(40, 157, 255)
    pdf.set_font("SimHei", size=20)
    pdf.cell(200, 10, txt="处理建议", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("SimHei", size=14)
    for idx, rec in enumerate(data["recommendations"], 1):
        pdf.multi_cell(0, 8, txt=f"{idx}. {rec}")  # 调整行高

    # 保存文件
    pdf.output(filepath)



@api_view(['POST'])
def generate_pdf(request):
    text = request.data.get("text", "")
    probability_str = request.data.get("probability", "0").strip()

    # 增强类型校验
    if not probability_str.replace('%', '').replace('.', '').isdigit():
        raise ValueError("概率值包含非法字符")

    probability = float(probability_str.replace('%', ''))
    generator = generators.ReportGenerator()
    try:
        analysis_result = generator.generate_analysis(text, probability)

        filename = generate_random_filename()
        reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, filename)
        save_to_pdf(analysis_result, filename, filepath)

        # 返回文件下载响应
        return FileResponse(
            open(filepath, 'rb'),
            as_attachment=True,
            filename=f"report_{filename}"
        )
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def index(request):
    return render(request, "index.html")  # 主页
