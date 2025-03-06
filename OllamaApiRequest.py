import os

import requests


def ollama_api_request(prompt):
    """
    调用Ollama API进行大模型请求
    """

    # 根据Ollama已部署的模型进行添加或修改
    models = {
        "DeepseekR1": "Deepseek-r1:32b",
    }
    try:
        url = os.environ.get("OLLAMA_API")
        payload = {
            "model": models["DeepseekR1"],  # 根据实际使用的模型修改
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(url, json=payload, timeout=(5, 300))
        print(response)
        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:
        print(f"Ollama API请求失败: {str(e)}")
        return None
