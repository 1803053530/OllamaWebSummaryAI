import os
import threading

import certifi

from OllamaApiRequest import ollama_api_request

import requests
from bs4 import BeautifulSoup
import chardet
from ProcessingLine import ProgressController

decoded_content = None


def fetch_webpage_content(url):
    global decoded_content, encoding
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # 获取二进制响应内容
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=certifi.where())
        except:
            print("方案一失败，正在尝试方案二进行网页爬取......")
            response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        raw_content = response.content

        # 检测编码（使用双重检测策略）
        detected_encoding = chardet.detect(raw_content)['encoding']

        # 优先尝试utf-8-sig（处理BOM头）
        for encoding in ['utf-8-sig', detected_encoding, 'gbk', 'gb18030', 'big5']:
            try:
                decoded_content = raw_content.decode(encoding, errors='replace')
                if 'æ' in decoded_content or 'å' in decoded_content:
                    continue  # 跳过产生乱码的编码
                break
            except UnicodeDecodeError:
                continue
        else:
            decoded_content = raw_content.decode('utf-8', errors='replace')

        # 使用正确的编码重新构建soup
        soup = BeautifulSoup(decoded_content, 'html.parser', from_encoding=encoding)

        # 移除不需要的元素
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'meta']):
            element.decompose()

        # 处理特殊空白字符
        text = soup.get_text(separator='\n', strip=True)
        text = text.replace('\u200b', '')  # 去除零宽空格
        text = text.encode('utf-8', 'ignore').decode('utf-8')  # 二次编码清洗

        return text[:3000]  # 默认在3000字符处截断内容，避免token过大

    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None


def process_webpages(urls):
    for url in urls:
        #  打印处理信息
        print(f"\n{'=' * 40}\nProcessing URL: {url}\n{'=' * 40}")

        #  获取网页内容
        content = fetch_webpage_content(url)
        if not content:
            print("内容抓取失败，跳过")
            continue

        #  显示原始内容
        print(f"\n网页原始内容:\n{'-' * 40}\n{content}\n{'-' * 40}")

        #  构造提示词
        prompt = f"""请根据以下网页内容进行关键信息提取：
        {content}
        请用中文总结该网页的核心内容，并列出最重要的三个要点。"""

        #  调用大模型
        print("\n大模型处理信息中:\n" + '-' * 40)

        # 初始化进度控制器
        pc = ProgressController()
        response = None
        error = None

        #  定义API请求线程的工作函数
        def api_request():
            nonlocal response, error
            try:
                # 实际发送请求
                response = ollama_api_request(prompt)
            except Exception as e:
                error = e
            finally:
                pc.complete()  # 无论成功失败都结束进度条

        #  启动进度条和API线程
        pc.start()
        request_thread = threading.Thread(target=api_request)
        request_thread.start()

        #  等待请求完成（最多60秒）
        request_thread.join(timeout=180)

        #  处理结果
        if error:
            print(f"\n处理失败: {str(error)}")
        elif response:
            print(f"\n处理结果:\n{response}")
        else:
            print("\n请求超时，未获得响应")

        #  最终确认完成
        pc.complete()


if __name__ == "__main__":
    # 在此处添加需要爬取的URL列表
    urls_to_process = [
        # "https://www.baidu.com"
    ]
    if not urls_to_process:
        print("请添加需要处理的网页URL!")
        exit()

    elif not os.environ.get("OLLAMA_API"):
        print("请正确配置您的ollama api 环境变量!")
        exit()

    process_webpages(urls_to_process)
