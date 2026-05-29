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
from model import roberta_detection
from model import xlsx_detection




ALLOWED_TYPES = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'text/plain': 'txt',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx'
}


@api_view(['POST'])
def roberta_file_analyze(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['file']

    try:
        # 方法1：使用python-magic检测真实文件类型
        mime = magic.Magic(mime=True)
        file_content = uploaded_file.read(1024)  # 读取文件前1024字节
        uploaded_file.seek(0)  # 重置文件指针

        real_mime_type = mime.from_buffer(file_content)

        # 方法2：获取声明的MIME类型
        declared_mime_type = uploaded_file.content_type

        # 获取文件扩展名
        file_name = uploaded_file.name.lower()
        _, file_ext = os.path.splitext(file_name)
        file_ext = file_ext[1:]  # 去掉点号

        # 验证文件类型
        file_type = ALLOWED_TYPES.get(real_mime_type, 'unknown')

        # 检查扩展名是否匹配
        valid_extension = ALLOWED_TYPES.get(real_mime_type) == file_ext

        if file_type == 'pdf':
            paragraphs = pdf_detection.getParagraphs(
                uploaded_file,
                # page_numbers=[2, 3], # 指定页面
                page_numbers=None,  # 加载全部页面
                min_line_length=1
            )
            answer = {}
            length = len(paragraphs)
            for i in range(length):
                probability = roberta_detection.predict(paragraphs[i])
                answer['i'] = {
                    'content': paragraphs[i],
                    'probability': probability[0] * 100
                }
                # 转换为所需的数组格式
                result_array = list(answer.values())

                # 使用DRF的Response返回，会自动转换为JSON
                return Response(result_array)
        elif file_type == 'doc' or file_type == 'docx':
            paragraphs = doc_detection.getParagraphs(
                uploaded_file,
                min_line_length=1
            )
            answer = {}
            length = len(paragraphs)
            for i in range(length):
                probability = roberta_detection.predict(paragraphs[i])
                answer['i'] = {
                    'content': paragraphs[i],
                    'probability': probability[0] * 100
                }
                # 转换为所需的数组格式
                result_array = list(answer.values())

                # 使用DRF的Response返回，会自动转换为JSON
                return Response(result_array)
        elif file_type == 'txt':
            paragraphs = txt_detection.getParagraphs(
                uploaded_file,
                min_line_length=1
            )
            answer = {}
            length = len(paragraphs)
            for i in range(length):
                probability = roberta_detection.predict(paragraphs[i])
                answer['i'] = {
                    'content': paragraphs[i],
                    'probability': probability[0] * 100
                }
                # 转换为所需的数组格式
                result_array = list(answer.values())

                # 使用DRF的Response返回，会自动转换为JSON
                return Response(result_array)
        elif file_type == 'xlsx':
            paragraphs = xlsx_detection.getParagraphs(uploaded_file)
            answer = {}
            length = len(paragraphs)
            for i in range(length):
                probability = roberta_detection.predict(paragraphs[i])
                answer['i'] = {
                    'content': paragraphs[i],
                    'probability': probability[0] * 100
                }
                # 转换为所需的数组格式
                result_array = list(answer.values())

                # 使用DRF的Response返回，会自动转换为JSON
                return Response(result_array)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            answer['i'] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
            result_array = list(answer.values())

            # 使用DRF的Response返回，会自动转换为JSON
            return Response(result_array)
    else:
        ai_probability = roberta_detection.predict(text)
        return Response({"probability": ai_probability[0] * 100})


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
            answer['i'] = {
                'content': paragraphs[i],
                'probability': probability[0] * 100
            }
            # 转换为所需的数组格式
            result_array = list(answer.values())

            # 使用DRF的Response返回，会自动转换为JSON
            return Response(result_array)