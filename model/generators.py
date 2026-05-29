from openai import OpenAI
import json
from django.conf import settings
from .exceptions import GenerationError
import time
import random

class ReportGenerator:
    def __init__(self):
        # 初始化OpenAI客户端，API密钥从环境变量获取
        self.client = OpenAI(base_url='https://xiaoai.plus/v1',
                             api_key='sk-nYX5lE98cTtmWti7RuMEzjZ7JCOWeJPemNoryJM5WRYJQKZo')
        self.default_model = "gpt-4-turbo"  # 最新版支持JSON格式强制输出
        self.max_retries = 3  # API调用重试次数

    def _build_prompt(self, content, probability):
        """构造结构化提示词"""
        return f"""
        作为专业事实核查员，请根据以下信息生成分析报告：

        **新闻内容（截取前1000字符）**:
        {content[:1000]}

        **虚假概率值**: {probability}%

        **必须严格遵循以下要求**:
        1. 输出为合法JSON格式，包含summary, risk_level, evidence, recommendations字段
        2. risk_level取值：high/medium/low
        3. evidence至少包含3条不同维度的验证结果
        4. 使用中文撰写，保持专业客观语气

        **示例模板**:
        {{
          "summary": "新闻概要...",
          "risk_level": "high",
          "evidence": [
            "信源问题：...",
            "数据矛盾：...",
            "逻辑漏洞：..."
          ],
          "recommendations": [
            "建议1：...",
            "建议2：..."
          ]
        }}
        """

    def _parse_response(self, raw_response):
        """解析并验证API响应"""
        try:
            data = json.loads(raw_response)
            # 字段完整性检查
            required_keys = {'summary', 'risk_level', 'evidence', 'recommendations'}
            if not required_keys.issubset(data.keys()):
                raise ValueError("Missing required fields")
            # 证据数量检查
            if len(data['evidence']) < 2:
                raise ValueError("Insufficient evidence points")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            raise GenerationError(f"解析失败: {str(e)}")

    def generate_analysis(self, news_content, fake_prob):
        """生成分析报告主方法"""
        prompt = self._build_prompt(news_content, fake_prob)

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.default_model,
                    messages=[{
                        "role": "system",
                        "content": "你是一个专业的事实核查分析系统"
                    }, {
                        "role": "user",
                        "content": prompt
                    }],
                    temperature=0.3,  # 控制创造性（0-2，值越低越确定）
                    max_tokens=1500,  # 控制输出长度
                    response_format={"type": "json_object"},  # 强制JSON格式
                    timeout=30  # 秒
                )
                raw_output = response.choices[0].message.content
                return self._parse_response(raw_output)

            except Exception as e:
                if '429' in str(e):
                    # 指数退避 + 随机抖动
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                if attempt == self.max_retries - 1:
                    raise GenerationError(f"生成失败，重试次数耗尽: {str(e)}")

        return {}  # 保证有返回值