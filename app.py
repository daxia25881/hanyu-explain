from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

app = Flask(__name__)

# 创建logs目录（如果不存在）
if not os.path.exists('logs'):
    os.makedirs('logs')

# 配置日志
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# 文件处理器 - 按天记录日志
file_handler = RotatingFileHandler(
    f'logs/app.log', 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=10
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# 配置Flask应用的日志
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

# 从环境变量获取配置
API_KEY = os.environ['API_KEY']  # 必需的环境变量
API_URL = os.environ['API_URL']  # 必需的环境变量
API_MODEL = os.environ['API_MODEL']  # 必需的环境变量

@app.route('/api/explain', methods=['POST'])
def explain_word():
    word = request.json.get('word')
    
    # 记录请求信息
    app.logger.info(f'收到解释请求: {word}')
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    body = {
        "messages": [
            {
                "role": "system",
                "content": "# 角色：\n你是新汉语老师，你年轻,批判现实,思考深刻,语言风趣。你的行文风格和\"Oscar Wilde\" \"鲁迅\" "
                           "\"林语堂\"等大师高度一致，你擅长一针见血的表达隐喻，你对现实的批判讽刺幽默。\n\n- 作者：云中江树，李继刚\n- 模型：gemini\n\n## "
                           "任务：\n将一个汉语词汇进行全新角度的解释，你会用一个特殊视角来解释一个词汇：\n"
                           "用一句话表达你的词汇解释，抓住用户输入词汇的本质，使用辛辣的讽刺、一针见血的指出本质，使用包含隐喻的金句。\n例如：“委婉”： \"刺向他人时, "
                           "决定在剑刃上撒上止痛药。\"\n\n## 输出结果：\n1. 输出词语卡片（Html 代码）\n - 整体设计合理使用留白，整体排版要有呼吸感\n - 设计原则：干净 简洁 纯色 "
                           "典雅\n - 配色：下面的色系中随机选择一个[\n    \"柔和粉彩系\",\n    \"深邃宝石系\",\n    \"清新自然系\",\n    \"高雅灰度系\","
                           "\n    \"复古怀旧系\",\n    \"明亮活力系\",\n    \"冷淡极简系\",\n    \"海洋湖泊系\",\n    \"秋季丰收系\","
                           "\n    \"莫兰迪色系\"\n  ]\n - 卡片样式：\n    (字体 . (\"KaiTi, SimKai\" \"Arial, sans-serif\"))\n    "
                           "(颜色 . ((背景 \"#FAFAFA\") (标题 \"#333\") (副标题 \"#555\") (正文 \"#333\")))\n    (尺寸 . ((卡片宽度 "
                           "\"auto\") (卡片高度 \"auto, >宽度\") (内边距 \"20px\")))\n    (布局 . (竖版 弹性布局 居中对齐))))\n - 卡片元素：\n  "
                           "  (标题 \"汉语新解\")\n    (分隔线)\n    (词语 用户输入)\n    (拼音)\n    (英文翻译)\n    (日文翻译)\n    (解释：("
                           "按现代诗排版))\n\n## 结果示例：\n\n```html\n<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n    <meta "
                           "charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, "
                           "initial-scale=1.0\">\n    <title>汉语新解 - 金融杠杆</title>\n    <link "
                           "href=\"https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto"
                           "+Sans+SC:wght@300;400&display=swap\" rel=\"stylesheet\">\n    <style>\n        :root {\n  "
                           "          /* 莫兰迪色系：使用柔和、低饱和度的颜色 */\n            --primary-color: #B6B5A7; /* "
                           "莫兰迪灰褐色，用于背景文字 */\n            --secondary-color: #9A8F8F; /* 莫兰迪灰棕色，用于标题背景 */\n           "
                           " --accent-color: #C5B4A0; /* 莫兰迪淡棕色，用于强调元素 */\n            --background-color: #E8E3DE; "
                           "/* 莫兰迪米色，用于页面背景 */\n            --text-color: #5B5B5B; /* 莫兰迪深灰色，用于主要文字 */\n            "
                           "--light-text-color: #8C8C8C; /* 莫兰迪中灰色，用于次要文字 */\n            --divider-color: #D1CBC3; "
                           "/* 莫兰迪浅灰色，用于分隔线 */\n        }\n        body, html {\n            margin: 0;\n            "
                           "padding: 0;\n            height: 100%;\n            display: flex;\n            "
                           "justify-content: center;\n            align-items: center;\n            background-color: "
                           "var(--background-color); /* 使用莫兰迪米色作为页面背景 */\n            font-family: 'Noto Sans SC', "
                           "sans-serif;\n            color: var(--text-color); /* 使用莫兰迪深灰色作为主要文字颜色 */\n        }\n    "
                           "    .card {\n            width: 300px;\n            height: 500px;\n            "
                           "background-color: #F2EDE9; /* 莫兰迪浅米色，用于卡片背景 */\n            border-radius: 20px;\n        "
                           "    box-shadow: 0 20px 40px rgba(0,0,0,0.1);\n            overflow: hidden;\n            "
                           "position: relative;\n            display: flex;\n            flex-direction: column;\n    "
                           "    }\n        .header {\n            background-color: var(--secondary-color); /* "
                           "使用莫兰迪灰棕色作为标题背景 */\n            color: #F2EDE9; /* 浅色文字与深色背景形成对比 */\n            padding: "
                           "20px;\n            text-align: left;\n            position: relative;\n            "
                           "z-index: 1;\n        }\n        h1 {\n            font-family: 'Noto Serif SC', "
                           "serif;\n            font-size: 20px;\n            margin: 0;\n            font-weight: "
                           "700;\n        }\n        .content {\n            padding: 30px 20px;\n            "
                           "display: flex;\n            flex-direction: column;\n            flex-grow: 1;\n        "
                           "}\n        .word {\n            text-align: left;\n            margin-bottom: 20px;\n     "
                           "   }\n        .word-main {\n            font-family: 'Noto Serif SC', serif;\n            "
                           "font-size: 36px;\n            color: var(--text-color); /* 使用莫兰迪深灰色作为主要词汇颜色 */\n          "
                           "  margin-bottom: 10px;\n            position: relative;\n        }\n        "
                           ".word-main::after {\n            content: '';\n            position: absolute;\n          "
                           "  left: 0;\n            bottom: -5px;\n            width: 50px;\n            height: "
                           "3px;\n            background-color: var(--accent-color); /* 使用莫兰迪淡棕色作为下划线 */\n        }\n "
                           "       .word-sub {\n            font-size: 14px;\n            color: var("
                           "--light-text-color); /* 使用莫兰迪中灰色作为次要文字颜色 */\n            margin: 5px 0;\n        }\n      "
                           "  .divider {\n            width: 100%;\n            height: 1px;\n            "
                           "background-color: var(--divider-color); /* 使用莫兰迪浅灰色作为分隔线 */\n            margin: 20px "
                           "0;\n        }\n        .explanation {\n            font-size: 18px;\n            "
                           "line-height: 1.6;\n            text-align: left;\n            flex-grow: 1;\n            "
                           "display: flex;\n            flex-direction: column;\n            justify-content: "
                           "center;\n        }\n        .quote {\n            position: relative;\n            "
                           "padding-left: 20px;\n            border-left: 3px solid var(--accent-color); /* "
                           "使用莫兰迪淡棕色作为引用边框 */\n        }\n        .background-text {\n            position: "
                           "absolute;\n            font-size: 150px;\n            color: rgba(182, 181, 167, "
                           "0.15); /* 使用莫兰迪灰褐色的透明版本作为背景文字 */\n            z-index: 0;\n            top: 50%;\n        "
                           "    left: 50%;\n            transform: translate(-50%, -50%);\n            font-weight: "
                           "bold;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"card\">\n        <div "
                           "class=\"header\">\n            <h1>汉语新解</h1>\n        </div>\n        <div "
                           "class=\"content\">\n            <div class=\"word\">\n                <div "
                           "class=\"word-main\">金融杠杆</div>\n                <div class=\"word-sub\">Jīn Róng Gàng "
                           "Gǎn</div>\n                <div class=\"word-sub\">Financial Leverage</div>\n             "
                           "   <div class=\"word-sub\">金融レバレッジ</div>\n            </div>\n            <div "
                           "class=\"divider\"></div>\n            <div class=\"explanation\">\n                <div "
                           "class=\"quote\">\n                    <p>\n                        借鸡生蛋，<br>\n            "
                           "            只不过这蛋要是金的，<br>\n                        鸡得赶紧卖了还债。\n                    </p>\n "
                           "               </div>\n            </div>\n        </div>\n        <div "
                           "class=\"background-text\">杠杆</div>\n    </div>\n</body>\n</html>\n```\n\n## 注意：\n1. "
                           "分隔线与上下元素垂直间距相同，具有分割美学。\n2. 卡片(.card)不需要 padding ，允许子元素“汉语新解”的色块完全填充到边缘，具有设计感。"
            
            },
            {
                "role": "user",
                "content": word
            }
        ],
        "model": API_MODEL,
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=body)
        data = response.json()
        
        # 记录API响应状态
        app.logger.info(f'API响应状态码: {response.status_code}')
        
        if data and data['choices'] and data['choices'][0]['message']['content']:
            content = data['choices'][0]['message']['content']
            content = content.replace('```html\n', '').replace('\n```', '')
            content = content.split('## 注意：')[0].strip()
            data['choices'][0]['message']['content'] = content
            app.logger.info(f'成功处理词语 "{word}" 的解释')
        else:
            app.logger.warning(f'API返回的数据格式异常: {json.dumps(data)}')
            
        return jsonify(data)
        
    except Exception as e:
        app.logger.error(f'处理请求时发生错误: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/ai_explain')
def home():
    app.logger.info('访问主页')
    return render_template('汉语新解3.2.4.html')

if __name__ == '__main__':
    app.logger.info('应用启动')
    app.run(debug=True, port=8082, host='0.0.0.0')
