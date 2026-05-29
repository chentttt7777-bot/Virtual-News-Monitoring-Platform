class GenerationError(Exception):
    def __init__(self, message):
        super().__init__(f"报告生成错误: {message}")