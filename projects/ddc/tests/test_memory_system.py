import os
import shutil
import pytest
from projects.ddc.brain.brain_core.limbic_system.working_memory import WorkingMemory
from projects.ddc.brain.brain_core.limbic_system.limbic_coordinator import LimbicCoordinator

def test_working_memory_persistence():
    user_id = "test_bot_1"
    # Clean up previous tests
    storage_dir = os.path.expanduser(f"~/.openclaw/memory/{user_id}")
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir)
        
    wm = WorkingMemory(user_id, capacity=3)
    wm.add_trace("user", "Hello")
    wm.add_trace("assistant", "Hi there")
    
    # Reload from disk
    wm_new = WorkingMemory(user_id, capacity=3)
    assert len(wm_new.traces) == 2
    assert wm_new.traces[0].content == "Hello"
    
    shutil.rmtree(storage_dir)

def test_working_memory_capacity():
    user_id = "test_bot_2"
    wm = WorkingMemory(user_id, capacity=2)
    wm.add_trace("user", "1")
    wm.add_trace("assistant", "2")
    wm.add_trace("user", "3")
    wm.add_trace("assistant", "4")
    wm.add_trace("user", "5") # Should evict 1, 2
    
    context = wm.get_context()
    assert "1" not in context
    assert "2" in context  # deque maxlen=4만 1개(1)가 나감
    assert "3" in context
    assert len(wm.traces) == 4
    
    storage_dir = os.path.expanduser(f"~/.openclaw/memory/{user_id}")
    shutil.rmtree(storage_dir)

@pytest.mark.asyncio
async def test_limbic_coordinator_context():
    user_id = "test_bot_3"
    coord = LimbicCoordinator(user_id)
    coord.record_interaction("user", "My name is SHawn")
    coord.record_interaction("assistant", "Nice to meet you, SHawn!")
    
    context = await coord.build_integrated_context("Tell me more", level="L3")
    assert "[Recent Conversation]" in context
    assert "SHawn" in context
    
    storage_dir = os.path.expanduser(f"~/.openclaw/memory/{user_id}")
    shutil.rmtree(storage_dir)

if __name__ == "__main__":
    pytest.main([__file__])
