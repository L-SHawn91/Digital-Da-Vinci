import asyncio
import os
import sys
import logging

# Set project root
sys.path.append(os.getcwd())

from projects.ddc.brain.brain_core.chat_engine import get_chat_engine

async def verify_chat_memory():
    print("🧠 Starting Memory Verification...")
    engine = get_chat_engine()
    user_id = 99999999 # Fake User
    
    # 1. First Turn: introduce something
    print("\nTurn 1: Providing information...")
    resp1 = await engine.get_response(user_id, "안녕? 난 숀브레인의 새로운 연구원 '철수'라고 해. 오늘 자궁 오가노이드 실험 결과가 아주 좋았어.")
    print(f"Bot: {resp1}")
    
    # 2. Second Turn: ask about previous context
    print("\nTurn 2: Checking short-term memory...")
    resp2 = await engine.get_response(user_id, "내 이름이 뭔지 기억나? 그리고 오늘 무슨 실험이 잘 됐다고 했지?")
    print(f"Bot: {resp2}")
    
    # Verification logic
    if "철수" in resp2 and "오가노이드" in resp2:
        print("\n✅ SUCCESS: Context maintained in WorkingMemory!")
    else:
        print("\n❌ FAILURE: Context lost or not retrieved correctly.")
        
    # 3. Third Turn: Salience Check
    print("\nTurn 3: Checking Amygdala (Importance)...")
    resp3 = await engine.get_response(user_id, "이건 진짜 중요한 버그인데, 시스템 좌표가 안 맞아! 빨리 확인해줘!")
    print(f"Bot: {resp3}")
    # ChatEngine logs should show high importance

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(verify_chat_memory())
