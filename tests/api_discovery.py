#!/usr/bin/env python3
"""
D-CNS API Discovery & Health Check
환경 변수 기반 가용 모델 자동 발굴 및 검증
"""

import os
import asyncio
import logging
from typing import Dict, List
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("APIDiscovery")

class APIDiscovery:
    """환경 변수 기반 API 키 검증 및 모델 발굴"""
    
    def __init__(self):
        self.available_engines = {}
        self.available_models = {}
        
    def scan_api_keys(self) -> Dict[str, str]:
        """환경 변수에서 API 키 스캔"""
        logger.info("🔍 환경 변수 스캔 중...")
        
        api_keys = {}
        key_patterns = {
            "GROQ_API_KEY": "Groq",
            "GEMINI_API_KEY": "Gemini",
            "ANTHROPIC_API_KEY": "Claude",
            "OPENAI_API_KEY": "OpenAI",
            "DEEPSEEK_API_KEY": "DeepSeek",
            "CEREBRAS_API_KEY": "Cerebras",
            "MISTRAL_API_KEY": "Mistral",
        }
        
        for env_var, engine_name in key_patterns.items():
            key = os.getenv(env_var)
            if key and len(key) > 10:  # 유효한 키인지 간단 검증
                api_keys[engine_name] = key
                logger.info(f"  ✅ {engine_name}: API 키 발견 ({key[:10]}...)")
            else:
                logger.info(f"  ❌ {engine_name}: API 키 없음")
        
        return api_keys
    
    async def discover_models(self, api_keys: Dict[str, str]) -> Dict[str, List[str]]:
        """각 엔진에서 사용 가능한 모델 목록 가져오기"""
        logger.info("\n🧠 가용 모델 발굴 중...")
        
        models = {}
        
        # Groq
        if "Groq" in api_keys:
            try:
                client = Groq(api_key=api_keys["Groq"])
                model_list = client.models.list()
                models["Groq"] = [m.id for m in model_list.data if "llama" in m.id.lower()]
                logger.info(f"  🟢 Groq: {len(models['Groq'])}개 모델 발견")
            except Exception as e:
                logger.error(f"  🔴 Groq 모델 조회 실패: {e}")
        
        # Gemini
        if "Gemini" in api_keys:
            try:
                genai.configure(api_key=api_keys["Gemini"])
                model_list = genai.list_models()
                models["Gemini"] = [m.name.replace("models/", "") for m in model_list if "generateContent" in m.supported_generation_methods]
                logger.info(f"  🟢 Gemini: {len(models['Gemini'])}개 모델 발견")
            except Exception as e:
                logger.error(f"  🔴 Gemini 모델 조회 실패: {e}")
        
        # Claude (하드코딩 - Anthropic API는 모델 리스트 엔드포인트 없음)
        if "Claude" in api_keys:
            models["Claude"] = [
                "claude-3-5-sonnet-20240620",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
            logger.info(f"  🟡 Claude: {len(models['Claude'])}개 모델 (하드코딩)")
        
        # OpenAI
        if "OpenAI" in api_keys:
            try:
                client = OpenAI(api_key=api_keys["OpenAI"])
                model_list = client.models.list()
                models["OpenAI"] = [m.id for m in model_list.data if any(x in m.id for x in ["gpt-4", "o1"])]
                logger.info(f"  🟢 OpenAI: {len(models['OpenAI'])}개 모델 발견")
            except Exception as e:
                logger.error(f"  🔴 OpenAI 모델 조회 실패: {e}")
        
        # DeepSeek
        if "DeepSeek" in api_keys:
            models["DeepSeek"] = ["deepseek-chat", "deepseek-coder"]
            logger.info(f"  🟡 DeepSeek: {len(models['DeepSeek'])}개 모델 (하드코딩)")
        
        # Cerebras
        if "Cerebras" in api_keys:
            models["Cerebras"] = ["llama3.1-70b", "llama3.1-8b"]
            logger.info(f"  🟡 Cerebras: {len(models['Cerebras'])}개 모델 (하드코딩)")
        
        # Mistral
        if "Mistral" in api_keys:
            models["Mistral"] = ["mistral-large-latest", "mistral-small-latest", "codestral-latest", "pixtral-12b-2409"]
            logger.info(f"  🟡 Mistral: {len(models['Mistral'])}개 모델 (하드코딩)")
        
        return models
    
    async def health_check(self, api_keys: Dict[str, str], models: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """각 모델에 Health Check 수행"""
        logger.info("\n💊 Health Check 수행 중...")
        
        healthy_models = {}
        
        for engine, model_list in models.items():
            healthy_models[engine] = []
            
            for model_id in model_list[:3]:  # 각 엔진당 최대 3개만 테스트 (시간 절약)
                try:
                    logger.info(f"  🧪 {engine}/{model_id} 테스트 중...")
                    
                    if engine == "Groq":
                        client = Groq(api_key=api_keys[engine])
                        client.chat.completions.create(
                            model=model_id,
                            messages=[{"role": "user", "content": "Hi"}],
                            max_tokens=5
                        )
                    elif engine == "Gemini":
                        model = genai.GenerativeModel(model_id)
                        model.generate_content("Hi")
                    elif engine == "Claude":
                        client = Anthropic(api_key=api_keys[engine])
                        client.messages.create(
                            model=model_id,
                            max_tokens=5,
                            messages=[{"role": "user", "content": "Hi"}]
                        )
                    elif engine in ["OpenAI", "DeepSeek", "Cerebras", "Mistral"]:
                        base_urls = {
                            "OpenAI": "https://api.openai.com/v1",
                            "DeepSeek": "https://api.deepseek.com",
                            "Cerebras": "https://api.cerebras.ai/v1",
                            "Mistral": "https://api.mistral.ai/v1"
                        }
                        client = OpenAI(api_key=api_keys[engine], base_url=base_urls.get(engine))
                        client.chat.completions.create(
                            model=model_id,
                            messages=[{"role": "user", "content": "Hi"}],
                            max_tokens=5
                        )
                    
                    healthy_models[engine].append(model_id)
                    logger.info(f"    ✅ 성공")
                    
                except Exception as e:
                    logger.error(f"    ❌ 실패: {str(e)[:50]}")
                
                await asyncio.sleep(1)  # Rate limit 방지
        
        return healthy_models

async def main():
    discovery = APIDiscovery()
    
    # 1. API 키 스캔
    api_keys = discovery.scan_api_keys()
    
    if not api_keys:
        logger.error("❌ 사용 가능한 API 키가 없습니다.")
        return
    
    # 2. 모델 발굴
    models = await discovery.discover_models(api_keys)
    
    # 3. Health Check
    healthy = await discovery.health_check(api_keys, models)
    
    # 4. 최종 보고
    logger.info("\n" + "="*80)
    logger.info("📊 최종 보고: 실제 작동하는 모델 목록")
    logger.info("="*80)
    
    total = 0
    for engine, model_list in healthy.items():
        logger.info(f"\n🟢 {engine}: {len(model_list)}개")
        for m in model_list:
            logger.info(f"  - {m}")
            total += 1
    
    logger.info(f"\n✅ 총 {total}개의 작동 가능한 모델 발견")

if __name__ == "__main__":
    asyncio.run(main())
