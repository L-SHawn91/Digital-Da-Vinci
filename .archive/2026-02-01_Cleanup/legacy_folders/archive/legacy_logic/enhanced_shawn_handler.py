"""
SHawn-BOT Handler Wrapper with Multi-Provider Integration
Integrates the MultiProviderRetryEngine with existing SHawn-BOT handlers
"""

import asyncio
import json
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import logging

from multi_provider_retry_engine import MultiProviderRetryEngine, ProviderConfig


class EnhancedShawnHandler:
    """
    Enhanced SHawn-BOT Handler with Multi-Provider Support
    - Automatic provider selection and fallback
    - Cost optimization
    - Performance tracking
    - Intelligent retry mechanisms
    """

    def __init__(self, original_handler_func: Callable, handler_name: str):
        self.original_handler = original_handler_func
        self.handler_name = handler_name
        self.retry_engine = MultiProviderRetryEngine()
        self.handler_stats = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "avg_response_time": 0.0,
            "total_cost_savings": 0.0,
            "last_provider_used": None,
            "call_history": [],
        }
        self.logger = logging.getLogger(f"Enhanced{handler_name}")

    async def handle_with_retry(
        self,
        request_data: Dict[str, Any],
        max_attempts: int = 5,
        timeout: int = 60,
        task_type: str = "general",
    ) -> Dict[str, Any]:
        """
        Enhanced handler with multi-provider retry capabilities
        """

        start_time = datetime.now()
        self.handler_stats["total_calls"] += 1

        # Create task function for the retry engine
        async def provider_task(
            provider_config: ProviderConfig, task_description: str
        ) -> Dict[str, Any]:
            """Execute the original handler with specific provider configuration"""

            # Inject provider configuration into request
            enhanced_request = {
                **request_data,
                "provider_config": {
                    "name": provider_config.name.value,
                    "api_key": provider_config.api_key,
                    "model": provider_config.model,
                    "base_url": provider_config.base_url,
                    "max_tokens": provider_config.max_tokens,
                    "timeout": provider_config.timeout,
                },
                "task_type": task_type,
                "handler_name": self.handler_name,
                "use_enhanced_mode": True,
            }

            # Call original handler with enhanced request
            try:
                result = await self.original_handler(enhanced_request)

                # Ensure result has required fields
                if isinstance(result, dict):
                    result["provider_used"] = provider_config.name.value
                    result["model_used"] = provider_config.model
                    result["handler_enhanced"] = True

                return result

            except Exception as e:
                # Re-raise with provider context
                raise Exception(f"{provider_config.name.value}: {str(e)}")

        # Execute with multi-provider retry
        task_description = f"{self.handler_name} handler - {task_type}"

        try:
            result = await self.retry_engine.execute_with_multi_provider_retry(
                provider_task,
                task_description,
                max_attempts=max_attempts,
                timeout=timeout,
            )

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # Update handler statistics
            if result["status"] == "success":
                self.handler_stats["successful_calls"] += 1
                self.handler_stats["last_provider_used"] = result["provider_used"]

                # Update average response time
                current_avg = self.handler_stats["avg_response_time"]
                successful_calls = self.handler_stats["successful_calls"]
                self.handler_stats["avg_response_time"] = (
                    current_avg * (successful_calls - 1) + execution_time
                ) / successful_calls

                # Add to call history
                history_entry = {
                    "timestamp": start_time.isoformat(),
                    "execution_time": execution_time,
                    "provider_used": result["provider_used"],
                    "attempts": result["attempts"],
                    "task_type": task_type,
                    "status": "success",
                }
            else:
                self.handler_stats["failed_calls"] += 1
                history_entry = {
                    "timestamp": start_time.isoformat(),
                    "execution_time": execution_time,
                    "providers_tried": result.get("providers_tried", []),
                    "attempts": result["attempts"],
                    "task_type": task_type,
                    "status": "failed",
                    "error": result.get("error", "Unknown error"),
                }

            self.handler_stats["call_history"].append(history_entry)

            # Keep only last 100 calls in history
            if len(self.handler_stats["call_history"]) > 100:
                self.handler_stats["call_history"] = self.handler_stats["call_history"][
                    -100:
                ]

            return result

        except Exception as e:
            # Handle unexpected errors
            self.handler_stats["failed_calls"] += 1
            self.logger.error(f"Unexpected error in {self.handler_name}: {str(e)}")

            return {
                "status": "failed",
                "error": f"Handler error: {str(e)}",
                "handler_name": self.handler_name,
                "execution_time": (datetime.now() - start_time).total_seconds(),
            }

    def get_handler_stats(self) -> Dict[str, Any]:
        """Get comprehensive handler statistics"""

        total_calls = self.handler_stats["total_calls"]
        success_rate = (
            self.handler_stats["successful_calls"] / max(total_calls, 1)
        ) * 100

        # Get provider stats from retry engine
        provider_stats = self.retry_engine.get_provider_stats()

        return {
            "handler_name": self.handler_name,
            "handler_stats": {
                **self.handler_stats,
                "success_rate": f"{success_rate:.1f}%",
            },
            "provider_stats": provider_stats,
            "performance_summary": {
                "total_calls": total_calls,
                "successful_calls": self.handler_stats["successful_calls"],
                "failed_calls": self.handler_stats["failed_calls"],
                "success_rate": f"{success_rate:.1f}%",
                "avg_response_time": f"{self.handler_stats['avg_response_time']:.2f}s",
            },
        }

    def get_recent_performance(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent performance summary"""

        recent_calls = self.handler_stats["call_history"][-limit:]

        if not recent_calls:
            return {"message": "No recent calls"}

        # Calculate recent metrics
        successful_recent = [c for c in recent_calls if c["status"] == "success"]
        recent_success_rate = (len(successful_recent) / len(recent_calls)) * 100

        avg_recent_time = sum(c["execution_time"] for c in recent_calls) / len(
            recent_calls
        )

        # Provider usage in recent calls
        provider_usage = {}
        for call in recent_calls:
            provider = call.get("provider_used", "unknown")
            provider_usage[provider] = provider_usage.get(provider, 0) + 1

        return {
            "recent_calls": len(recent_calls),
            "recent_success_rate": f"{recent_success_rate:.1f}%",
            "avg_recent_time": f"{avg_recent_time:.2f}s",
            "provider_usage": provider_usage,
            "last_calls": recent_calls,
        }

    def reset_handler_stats(self):
        """Reset handler statistics"""
        self.handler_stats = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "avg_response_time": 0.0,
            "total_cost_savings": 0.0,
            "last_provider_used": None,
            "call_history": [],
        }
        self.retry_engine.reset_provider_stats()
        self.logger.info(f"Statistics reset for {self.handler_name}")


class HandlerManager:
    """
    Manager for multiple enhanced handlers
    """

    def __init__(self):
        self.handlers: Dict[str, EnhancedShawnHandler] = {}
        self.manager_stats = {
            "total_handlers": 0,
            "active_handlers": 0,
            "total_requests": 0,
            "manager_start_time": datetime.now(),
        }

    def register_handler(self, handler_name: str, original_handler_func: Callable):
        """Register a new enhanced handler"""

        enhanced_handler = EnhancedShawnHandler(original_handler_func, handler_name)
        self.handlers[handler_name] = enhanced_handler
        self.manager_stats["total_handlers"] += 1
        self.manager_stats["active_handlers"] += 1

        print(f"✅ Registered enhanced handler: {handler_name}")

        return enhanced_handler

    async def execute_handler(
        self, handler_name: str, request_data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        """Execute a specific enhanced handler"""

        if handler_name not in self.handlers:
            return {
                "status": "failed",
                "error": f"Handler '{handler_name}' not registered",
            }

        self.manager_stats["total_requests"] += 1

        handler = self.handlers[handler_name]
        return await handler.handle_with_retry(request_data, **kwargs)

    def get_all_handler_stats(self) -> Dict[str, Any]:
        """Get statistics for all registered handlers"""

        all_stats = {
            "manager_stats": {
                **self.manager_stats,
                "manager_uptime": str(
                    datetime.now() - self.manager_stats["manager_start_time"]
                ),
            },
            "handler_summaries": {},
            "detailed_handler_stats": {},
        }

        # Calculate overall metrics
        total_calls = sum(
            h.handler_stats["total_calls"] for h in self.handlers.values()
        )
        total_successful = sum(
            h.handler_stats["successful_calls"] for h in self.handlers.values()
        )
        overall_success_rate = (total_successful / max(total_calls, 1)) * 100

        all_stats["overall_metrics"] = {
            "total_calls": total_calls,
            "successful_calls": total_successful,
            "overall_success_rate": f"{overall_success_rate:.1f}%",
            "registered_handlers": len(self.handlers),
        }

        # Individual handler stats
        for handler_name, handler in self.handlers.items():
            handler_stats = handler.get_handler_stats()
            all_stats["handler_summaries"][handler_name] = handler_stats[
                "performance_summary"
            ]
            all_stats["detailed_handler_stats"][handler_name] = handler_stats

        return all_stats

    def get_handler(self, handler_name: str) -> Optional[EnhancedShawnHandler]:
        """Get a specific enhanced handler"""
        return self.handlers.get(handler_name)


# Example usage and test functions
async def example_original_handler(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Example original SHawn-BOT handler"""

    provider_config = request_data.get("provider_config", {})
    task_type = request_data.get("task_type", "general")

    # Simulate processing time
    await asyncio.sleep(0.5)

    # Simulate 85% success rate
    import random

    if random.random() < 0.85:
        return {
            "status": "success",
            "content": f"Processed {task_type} task using {provider_config.get('name', 'unknown')}",
            "confidence": 0.92,
            "tokens_used": random.randint(50, 500),
            "response_time": 0.5,
        }
    else:
        raise Exception("Simulated handler failure")


async def test_enhanced_handlers():
    """Test the enhanced handler system"""

    print("🚀 Testing Enhanced SHawn-BOT Handlers")
    print("=" * 50)

    # Create handler manager
    manager = HandlerManager()

    # Register enhanced handlers
    research_handler = manager.register_handler("research", example_original_handler)
    analysis_handler = manager.register_handler("analysis", example_original_handler)
    content_handler = manager.register_handler("content", example_original_handler)

    print(f"📊 Registered {len(manager.handlers)} enhanced handlers")

    # Test different handlers
    test_requests = [
        {
            "handler": "research",
            "data": {"query": "AI market trends analysis", "task_type": "research"},
            "task_type": "research",
        },
        {
            "handler": "analysis",
            "data": {"query": "Financial data analysis", "task_type": "analysis"},
            "task_type": "analysis",
        },
        {
            "handler": "content",
            "data": {"query": "Generate blog content", "task_type": "content"},
            "task_type": "content",
        },
        {
            "handler": "research",
            "data": {"query": "Literature review on AI", "task_type": "research"},
            "task_type": "research",
        },
    ]

    print(f"\n🧪 Running {len(test_requests)} test requests...")
    print("-" * 50)

    results = []
    for i, test_req in enumerate(test_requests, 1):
        handler_name = test_req["handler"]
        request_data = test_req["data"]
        task_type = test_req["task_type"]

        print(f"\n📝 Request {i}: {handler_name} handler - {task_type}")

        result = await manager.execute_handler(
            handler_name, request_data, task_type=task_type, max_attempts=3
        )

        results.append(result)

        if result["status"] == "success":
            print(
                f"✅ Success with {result['provider_used']} in {result['attempts']} attempts"
            )
            print(f"   Time: {result['execution_time']:.2f}s")
        else:
            print(f"❌ Failed after {result['attempts']} attempts")
            print(f"   Error: {result['error']}")

    # Show comprehensive statistics
    print("\n📈 Comprehensive Statistics:")
    all_stats = manager.get_all_handler_stats()

    print(
        f"  Overall Success Rate: {all_stats['overall_metrics']['overall_success_rate']}"
    )
    print(f"  Total Requests: {all_stats['overall_metrics']['total_calls']}")
    print(f"  Manager Uptime: {all_stats['manager_stats']['manager_uptime']}")

    print("\n🏆 Handler Performance:")
    for handler_name, summary in all_stats["handler_summaries"].items():
        print(
            f"  {handler_name}: {summary['success_rate']} ({summary['total_calls']} calls, {summary['avg_response_time']})"
        )

    # Show recent performance for research handler
    if "research" in manager.handlers:
        print("\n📊 Recent Research Handler Performance:")
        recent_stats = manager.get_handler("research").get_recent_performance(5)
        if "recent_calls" in recent_stats:
            print(f"  Recent Success Rate: {recent_stats['recent_success_rate']}")
            print(f"  Avg Recent Time: {recent_stats['avg_recent_time']}")
            print(f"  Provider Usage: {recent_stats['provider_usage']}")

    return results


if __name__ == "__main__":
    asyncio.run(test_enhanced_handlers())
