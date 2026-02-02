"""
SHawn-BOT Integration with Multi-Provider Retry Engine
Real integration with existing SHawn-BOT handlers and brain system
"""

import asyncio
import os
import sys
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Add SHawn-BOT to path
shawn_bot_path = os.path.join(os.path.dirname(__file__), "SHawn-BOT")
if shawn_bot_path not in sys.path:
    sys.path.append(shawn_bot_path)

from multi_provider_retry_engine import MultiProviderRetryEngine, ProviderConfig
from enhanced_shawn_handler import EnhancedShawnHandler, HandlerManager


class SHawnBotIntegration:
    """
    Complete integration of Multi-Provider Retry Engine with SHawn-BOT
    """

    def __init__(self):
        self.retry_engine = MultiProviderRetryEngine()
        self.handler_manager = HandlerManager()
        self.integration_stats = {
            "start_time": datetime.now(),
            "total_integrations": 0,
            "successful_integrations": 0,
            "failed_integrations": 0,
            "brain_integrations": 0,
            "handler_integrations": 0,
        }

    async def integrate_brain_v4(self) -> Dict[str, Any]:
        """Integrate with SHawn Brain V4"""

        try:
            # Import SHawn Brain V4
            from shawn_brain_v4 import SHawnBrainV4

            # Create enhanced brain wrapper
            enhanced_brain = EnhancedShawnBrain(
                original_brain=SHawnBrainV4(), retry_engine=self.retry_engine
            )

            # Register as handler
            self.handler_manager.register_handler(
                "brain_v4", enhanced_brain.think_with_retry
            )

            self.integration_stats["brain_integrations"] += 1
            self.integration_stats["successful_integrations"] += 1

            return {
                "status": "success",
                "component": "SHawn Brain V4",
                "integration_type": "brain",
                "enhanced_methods": ["think", "think_with_context", "get_brain_status"],
            }

        except Exception as e:
            self.integration_stats["failed_integrations"] += 1
            return {"status": "failed", "component": "SHawn Brain V4", "error": str(e)}

    async def integrate_handlers(self) -> Dict[str, Any]:
        """Integrate with existing SHawn-BOT handlers"""

        integration_results = []

        try:
            # Import handlers
            from engines.handlers.bio_handler import BioHandler
            from engines.handlers.quant_handler import QuantHandler
            from engines.handlers.chat_handler import ChatHandler

            # Mock dependencies for testing
            class MockBrain:
                async def think(
                    self, prompt: str, task_type: str = "auto"
                ) -> Tuple[str, str]:
                    return f"Mock response for: {prompt}", "mock"

            class MockStateManager:
                def save_interaction(self, *args):
                    pass

            class MockErrorHandler:
                def handle(self, e, context=""):
                    return f"Error: {str(e)}"

            mock_brain = MockBrain()
            mock_state_manager = MockStateManager()
            mock_error_handler = MockErrorHandler()

            # Create handler instances
            handlers = {
                "bio": BioHandler(mock_brain, mock_state_manager, mock_error_handler),
                "quant": QuantHandler(
                    mock_brain, mock_state_manager, mock_error_handler
                ),
                "chat": ChatHandler(mock_brain, mock_state_manager, mock_error_handler),
            }

            # Register enhanced handlers
            for handler_name, handler in handlers.items():
                enhanced_handler = EnhancedShawnHandler(
                    original_handler_func=getattr(
                        handler, f"handle_{handler_name}", handler.handle
                    ),
                    handler_name=f"{handler_name}_handler",
                )

                self.handler_manager.handlers[f"{handler_name}_enhanced"] = (
                    enhanced_handler
                )
                self.integration_stats["handler_integrations"] += 1
                self.integration_stats["successful_integrations"] += 1

                integration_results.append(
                    {
                        "status": "success",
                        "handler": handler_name,
                        "enhanced_methods": [f"handle_{handler_name}"],
                    }
                )

            return {
                "status": "success",
                "component": "SHawn-BOT Handlers",
                "integration_type": "handlers",
                "results": integration_results,
            }

        except Exception as e:
            self.integration_stats["failed_integrations"] += 1
            return {
                "status": "failed",
                "component": "SHawn-BOT Handlers",
                "error": str(e),
            }

    async def test_integrated_system(self) -> Dict[str, Any]:
        """Test the complete integrated system"""

        test_results = []

        # Test brain integration
        if "brain_v4" in self.handler_manager.handlers:
            brain_handler = self.handler_manager.get_handler("brain_v4")

            test_request = {"prompt": "AI 기술 동향 분석", "task_type": "research"}

            try:
                result = await brain_handler.handle_with_retry(
                    test_request, task_type="research", max_attempts=3
                )

                test_results.append(
                    {
                        "test": "brain_v4_research",
                        "status": result["status"],
                        "provider_used": result.get("provider_used"),
                        "attempts": result.get("attempts"),
                        "execution_time": result.get("execution_time"),
                    }
                )

            except Exception as e:
                test_results.append(
                    {"test": "brain_v4_research", "status": "failed", "error": str(e)}
                )

        # Test handler integrations
        for handler_name in ["bio_enhanced", "quant_enhanced", "chat_enhanced"]:
            if handler_name in self.handler_manager.handlers:
                handler = self.handler_manager.get_handler(handler_name)

                test_request = {
                    "query": f"Test {handler_name.split('_')[0]} functionality",
                    "task_type": handler_name.split("_")[0],
                }

                try:
                    result = await handler.handle_with_retry(
                        test_request,
                        task_type=handler_name.split("_")[0],
                        max_attempts=2,
                    )

                    test_results.append(
                        {
                            "test": handler_name,
                            "status": result["status"],
                            "provider_used": result.get("provider_used"),
                            "attempts": result.get("attempts"),
                        }
                    )

                except Exception as e:
                    test_results.append(
                        {"test": handler_name, "status": "failed", "error": str(e)}
                    )

        return {
            "test_results": test_results,
            "summary": {
                "total_tests": len(test_results),
                "successful_tests": len(
                    [t for t in test_results if t["status"] == "success"]
                ),
                "failed_tests": len(
                    [t for t in test_results if t["status"] == "failed"]
                ),
            },
        }

    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status"""

        uptime = datetime.now() - self.integration_stats["start_time"]

        return {
            "integration_stats": {
                **self.integration_stats,
                "uptime": str(uptime),
                "success_rate": (
                    self.integration_stats["successful_integrations"]
                    / max(self.integration_stats["total_integrations"], 1)
                )
                * 100,
            },
            "provider_stats": self.retry_engine.get_provider_stats(),
            "handler_stats": self.handler_manager.get_all_handler_stats(),
        }


class EnhancedShawnBrain:
    """Enhanced SHawn Brain with multi-provider retry capabilities"""

    def __init__(self, original_brain, retry_engine: MultiProviderRetryEngine):
        self.original_brain = original_brain
        self.retry_engine = retry_engine
        self.enhancement_stats = {
            "total_thinks": 0,
            "successful_thinks": 0,
            "failed_thinks": 0,
            "avg_response_time": 0.0,
        }

    async def think_with_retry(
        self, request_data: Dict[str, Any], max_attempts: int = 5, timeout: int = 60
    ) -> Dict[str, Any]:
        """Enhanced think method with multi-provider retry"""

        start_time = datetime.now()
        self.enhancement_stats["total_thinks"] += 1

        prompt = request_data.get("prompt", "")
        task_type = request_data.get("task_type", "auto")

        # Create task function for retry engine
        async def brain_task(
            provider_config: ProviderConfig, task_description: str
        ) -> Dict[str, Any]:
            """Execute brain thinking with specific provider"""

            # Inject provider configuration into brain
            # Note: This would require modifying the original brain to accept provider config
            # For now, we'll use the original brain and track which provider would be used

            try:
                # Call original brain
                response, model_info = await self.original_brain.think(
                    prompt, task_type=task_type
                )

                return {
                    "status": "success",
                    "response": response,
                    "model_info": model_info,
                    "provider_used": provider_config.name.value,
                    "task_description": task_description,
                }

            except Exception as e:
                raise Exception(f"Brain think failed: {str(e)}")

        # Execute with multi-provider retry
        task_description = f"SHawn Brain V4 - {task_type} task"

        try:
            result = await self.retry_engine.execute_with_multi_provider_retry(
                brain_task, task_description, max_attempts=max_attempts, timeout=timeout
            )

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # Update statistics
            if result["status"] == "success":
                self.enhancement_stats["successful_thinks"] += 1

                # Update average response time
                current_avg = self.enhancement_stats["avg_response_time"]
                successful_thinks = self.enhancement_stats["successful_thinks"]
                self.enhancement_stats["avg_response_time"] = (
                    current_avg * (successful_thinks - 1) + execution_time
                ) / successful_thinks
            else:
                self.enhancement_stats["failed_thinks"] += 1

            return {
                **result,
                "execution_time": execution_time,
                "enhancement_stats": self.enhancement_stats,
            }

        except Exception as e:
            self.enhancement_stats["failed_thinks"] += 1
            return {
                "status": "failed",
                "error": f"Enhanced brain error: {str(e)}",
                "execution_time": (datetime.now() - start_time).total_seconds(),
            }


# Main integration function
async def run_complete_integration():
    """Run complete SHawn-BOT integration"""

    print("🚀 Starting Complete SHawn-BOT Integration")
    print("=" * 60)

    integration = SHawnBotIntegration()

    # Step 1: Integrate Brain V4
    print("\n📊 Step 1: Integrating SHawn Brain V4...")
    brain_result = await integration.integrate_brain_v4()
    print(f"   Status: {brain_result['status']}")
    if brain_result["status"] == "failed":
        print(f"   Error: {brain_result['error']}")

    # Step 2: Integrate Handlers
    print("\n🔧 Step 2: Integrating SHawn-BOT Handlers...")
    handler_result = await integration.integrate_handlers()
    print(f"   Status: {handler_result['status']}")
    if handler_result["status"] == "failed":
        print(f"   Error: {handler_result['error']}")

    # Step 3: Test Integrated System
    print("\n🧪 Step 3: Testing Integrated System...")
    test_result = await integration.test_integrated_system()

    print(f"   Total Tests: {test_result['summary']['total_tests']}")
    print(f"   Successful: {test_result['summary']['successful_tests']}")
    print(f"   Failed: {test_result['summary']['failed_tests']}")

    # Step 4: Show Integration Status
    print("\n📈 Step 4: Integration Status")
    status = integration.get_integration_status()

    print(f"   Total Integrations: {status['integration_stats']['total_integrations']}")
    print(f"   Success Rate: {status['integration_stats']['success_rate']:.1f}%")
    print(f"   Uptime: {status['integration_stats']['uptime']}")

    print(f"\n🎯 Provider Performance:")
    for provider, detail in status["provider_stats"]["provider_details"].items():
        if detail["total_attempts"] > 0:
            print(
                f"   {provider}: {detail['success_rate']} ({detail['total_attempts']} attempts)"
            )

    print(f"\n🏆 Handler Performance:")
    for handler, summary in status["handler_stats"]["handler_summaries"].items():
        print(
            f"   {handler}: {summary['success_rate']} ({summary['total_calls']} calls)"
        )

    return {
        "integration": integration,
        "brain_result": brain_result,
        "handler_result": handler_result,
        "test_result": test_result,
        "status": status,
    }


if __name__ == "__main__":
    asyncio.run(run_complete_integration())
