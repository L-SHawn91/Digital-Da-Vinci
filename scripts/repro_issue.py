
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from projects.ddc.brain.brain_core.chat_engine import get_chat_engine
from projects.ddc.brain.brain_core.intent_classifier import IntentType

async def main():
    print("🚀 Initializing ChatEngine...")
    engine = get_chat_engine()
    
    # Mock admin ID if not set
    if not os.getenv("ADMIN_USER_ID"):
        os.environ["ADMIN_USER_ID"] = "12345678"
        engine.admin_id = 12345678

    print("🔎 Initializing candidates...")
    await engine.initialize()
    
    print("\n🧪 Testing '오가노이드' query...")
    user_id = 12345678
    query = "오가노이드"
    
    try:
        # 1. Check Intent
        print(f"   [Intent Check]")
        cartridge = engine.get_cartridge(user_id)
        intent = engine._intent_classifier.classify(query, intent_history=cartridge._intent_history, user_profile=cartridge.profile.to_dict())
        print(f"   Intent: {intent.intent_type}, Target: {intent.target}, Confidence: {intent.confidence}")
        
        # 2. Get Response
        response = await engine.get_response(user_id, query)
        print(f"\n🤖 Response:\n{response}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
