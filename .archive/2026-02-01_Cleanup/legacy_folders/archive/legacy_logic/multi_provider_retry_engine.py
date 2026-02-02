"""
Multi-Provider SimpleRetryEngine for SHawn-BOT + OMO/Opencode Integration
Leverages all available API keys for robust retry and fallback strategies
"""

import asyncio
import random
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import os
from datetime import datetime


class ProviderType(Enum):
    """AI Provider Types"""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GROQ = "groq"
    CEREBRAS = "cerebras"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    JINA = "jina"
    MISTRAL = "mistral"
    OPENROUTER = "openrouter"
    SAMBANOVA = "sambanova"


@dataclass
class ProviderConfig:
    """Provider Configuration"""

    name: ProviderType
    api_key: str
    base_url: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 4096
    timeout: int = 30
    retry_count: int = 0
    success_count: int = 0
    last_used: Optional[datetime] = None
    is_available: bool = True


class MultiProviderRetryEngine:
    """
    Advanced Multi-Provider Retry Engine
    - Automatic provider selection based on success rates
    - Intelligent fallback strategies
    - Load balancing across providers
    - Cost optimization
    """

    def __init__(self):
        self.providers: Dict[ProviderType, ProviderConfig] = {}
        self.provider_priority: List[ProviderType] = []
        self.session_stats: Dict[str, Any] = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
            "cost_savings": 0.0,
        }
        self._initialize_providers()
        self._update_provider_priority()

    def _initialize_providers(self):
        """Initialize all available providers from environment variables"""

        # Provider configurations with optimal settings
        provider_configs = {
            ProviderType.ANTHROPIC: {
                "model": "claude-3-5-sonnet-20241022",
                "base_url": "https://api.anthropic.com",
                "cost_per_1k_tokens": 0.003,
            },
            ProviderType.OPENAI: {
                "model": "gpt-4o-mini",
                "base_url": "https://api.openai.com/v1",
                "cost_per_1k_tokens": 0.00015,
            },
            ProviderType.GROQ: {
                "model": "llama-3.1-70b-versatile",
                "base_url": "https://api.groq.com/openai/v1",
                "cost_per_1k_tokens": 0.00059,
            },
            ProviderType.CEREBRAS: {
                "model": "llama3.1-70b",
                "base_url": "https://api.cerebras.ai/v1",
                "cost_per_1k_tokens": 0.0008,
            },
            ProviderType.DEEPSEEK: {
                "model": "deepseek-chat",
                "base_url": "https://api.deepseek.com",
                "cost_per_1k_tokens": 0.00014,
            },
            ProviderType.GEMINI: {
                "model": "gemini-1.5-flash",
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "cost_per_1k_tokens": 0.000075,
            },
            ProviderType.JINA: {
                "model": "jina-r1:1.8b",
                "base_url": "https://api.jina.ai/v1",
                "cost_per_1k_tokens": 0.00025,
            },
            ProviderType.MISTRAL: {
                "model": "mistral-tiny",
                "base_url": "https://api.mistral.ai/v1",
                "cost_per_1k_tokens": 0.00025,
            },
            ProviderType.OPENROUTER: {
                "model": "meta-llama/llama-3.1-70b-instruct:free",
                "base_url": "https://openrouter.ai/api/v1",
                "cost_per_1k_tokens": 0.0,  # Free tier
            },
            ProviderType.SAMBANOVA: {
                "model": "Meta-Llama-3.1-70B-Instruct",
                "base_url": "https://api.sambanova.ai/v1",
                "cost_per_1k_tokens": 0.0005,
            },
        }

        # Initialize providers with API keys
        for provider_type, config in provider_configs.items():
            api_key = os.getenv(f"{provider_type.value.upper()}_API_KEY")
            if api_key:
                self.providers[provider_type] = ProviderConfig(
                    name=provider_type,
                    api_key=api_key,
                    base_url=config["base_url"],
                    model=config["model"],
                    max_tokens=4096,
                    timeout=30,
                )
                print(f"✅ Initialized {provider_type.value} provider")

    def _update_provider_priority(self):
        """Update provider priority based on success rates and cost"""

        def calculate_priority_score(provider: ProviderConfig) -> float:
            """Calculate priority score for provider selection"""

            # Success rate (70% weight)
            total_attempts = provider.success_count + provider.retry_count
            success_rate = provider.success_count / max(total_attempts, 1)

            # Cost optimization (20% weight) - lower cost = higher score
            cost_scores = {
                ProviderType.GEMINI: 1.0,
                ProviderType.DEEPSEEK: 0.9,
                ProviderType.OPENAI: 0.8,
                ProviderType.JINA: 0.7,
                ProviderType.MISTRAL: 0.7,
                ProviderType.SAMBANOVA: 0.6,
                ProviderType.GROQ: 0.5,
                ProviderType.CEREBRAS: 0.4,
                ProviderType.ANTHROPIC: 0.3,
                ProviderType.OPENROUTER: 0.2,  # Free tier bonus
            }
            cost_score = cost_scores.get(provider.name, 0.5)

            # Recency bonus (10% weight) - recently used providers get slight bonus
            recency_bonus = 0.0
            if provider.last_used:
                time_since_last = (datetime.now() - provider.last_used).total_seconds()
                if time_since_last < 300:  # Used within 5 minutes
                    recency_bonus = 0.1

            return (success_rate * 0.7) + (cost_score * 0.2) + (recency_bonus * 0.1)

        # Sort providers by priority score
        available_providers = [p for p in self.providers.values() if p.is_available]
        sorted_providers = sorted(
            available_providers, key=calculate_priority_score, reverse=True
        )

        # Update provider names list
        self.provider_priority = [p.name for p in sorted_providers]

    async def execute_with_multi_provider_retry(
        self,
        task_func: Callable,
        task_description: str,
        max_attempts: int = 5,
        timeout: int = 60,
    ) -> Dict[str, Any]:
        """
        Execute task with intelligent multi-provider retry strategy
        """

        start_time = time.time()
        attempt = 0
        last_error = None
        providers_tried = set()

        self.session_stats["total_requests"] += 1

        while attempt < max_attempts:
            attempt += 1

            # Select best available provider
            selected_provider = self._select_best_provider(providers_tried)

            if not selected_provider:
                break

            providers_tried.add(selected_provider.name)
            provider_config = self.providers[selected_provider.name]

            print(
                f"🔄 Attempt {attempt}/{max_attempts} using {selected_provider.name.value}"
            )

            try:
                # Execute task with selected provider
                result = await asyncio.wait_for(
                    task_func(provider_config, task_description), timeout=timeout
                )

                # Success! Update statistics
                execution_time = time.time() - start_time
                provider_config.success_count += 1
                provider_config.last_used = datetime.now()

                self.session_stats["successful_requests"] += 1
                self.session_stats["avg_response_time"] = (
                    self.session_stats["avg_response_time"]
                    * (self.session_stats["successful_requests"] - 1)
                    + execution_time
                ) / self.session_stats["successful_requests"]

                # Update provider priority
                self._update_provider_priority()

                return {
                    "status": "success",
                    "result": result,
                    "provider_used": selected_provider.name.value,
                    "attempts": attempt,
                    "execution_time": execution_time,
                    "providers_tried": [p.value for p in providers_tried],
                }

            except asyncio.TimeoutError:
                last_error = f"Timeout with {selected_provider.name.value}"
                provider_config.retry_count += 1
                print(f"⏰ {last_error}")

            except Exception as e:
                last_error = f"Error with {selected_provider.name.value}: {str(e)}"
                provider_config.retry_count += 1
                print(f"❌ {last_error}")

                # Mark provider as temporarily unavailable if it fails repeatedly
                if provider_config.retry_count > 3:
                    provider_config.is_available = False
                    print(
                        f"🚫 {selected_provider.name.value} marked as temporarily unavailable"
                    )

            # Exponential backoff with jitter
            if attempt < max_attempts:
                backoff_time = min(2**attempt, 30) + random.uniform(0, 1)
                await asyncio.sleep(backoff_time)

        # All attempts failed
        self.session_stats["failed_requests"] += 1

        return {
            "status": "failed",
            "error": last_error or "All providers failed",
            "attempts": attempt,
            "providers_tried": [p.value for p in providers_tried],
            "execution_time": time.time() - start_time,
        }

    def _select_best_provider(self, providers_tried: set) -> Optional[ProviderConfig]:
        """Select the best available provider that hasn't been tried"""

        for provider_name in self.provider_priority:
            if provider_name not in providers_tried:
                provider = self.providers.get(provider_name)
                if provider and provider.is_available:
                    return provider

        # If all priority providers have been tried, try any available provider
        for provider in self.providers.values():
            if provider.name not in providers_tried and provider.is_available:
                return provider

        return None

    def get_provider_stats(self) -> Dict[str, Any]:
        """Get detailed provider statistics"""

        stats = {
            "total_providers": len(self.providers),
            "available_providers": len(
                [p for p in self.providers.values() if p.is_available]
            ),
            "provider_details": {},
            "session_stats": self.session_stats,
            "provider_priority": [p.value for p in self.provider_priority[:5]],
        }

        for provider_name, provider in self.providers.items():
            total_attempts = provider.success_count + provider.retry_count
            success_rate = provider.success_count / max(total_attempts, 1)

            stats["provider_details"][provider_name.value] = {
                "success_rate": f"{success_rate:.2%}",
                "total_attempts": total_attempts,
                "successes": provider.success_count,
                "failures": provider.retry_count,
                "last_used": provider.last_used.isoformat()
                if provider.last_used
                else None,
                "is_available": provider.is_available,
                "model": provider.model,
            }

        return stats

    def reset_provider_stats(self):
        """Reset all provider statistics"""
        for provider in self.providers.values():
            provider.success_count = 0
            provider.retry_count = 0
            provider.last_used = None
            provider.is_available = True

        self.session_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
            "cost_savings": 0.0,
        }

        self._update_provider_priority()
        print("🔄 All provider statistics have been reset")


# Example usage and test functions
async def example_task_function(
    provider_config: ProviderConfig, task_description: str
) -> Dict[str, Any]:
    """
    Example task function that simulates API call to provider
    """

    # Simulate API call with random success/failure
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate network latency

    # 85% success rate for demonstration
    if random.random() < 0.85:
        return {
            "content": f"Response from {provider_config.name.value} for task: {task_description}",
            "model": provider_config.model,
            "tokens_used": random.randint(100, 1000),
            "cost": random.uniform(0.0001, 0.01),
        }
    else:
        raise Exception(f"Simulated API failure from {provider_config.name.value}")


# Test function
async def test_multi_provider_engine():
    """Test the multi-provider retry engine"""

    print("🚀 Testing Multi-Provider Retry Engine")
    print("=" * 50)

    engine = MultiProviderRetryEngine()

    # Show initial provider stats
    print("\n📊 Initial Provider Configuration:")
    stats = engine.get_provider_stats()
    for provider, detail in stats["provider_details"].items():
        print(f"  {provider}: {detail['model']} ({detail['is_available']})")

    print(f"\n🎯 Provider Priority: {stats['provider_priority'][:5]}")

    # Test with multiple tasks
    test_tasks = [
        "Analyze the market trends for AI providers",
        "Generate a summary of multi-provider strategies",
        "Compare cost optimization techniques",
        "Evaluate fallback mechanisms",
    ]

    print(f"\n🧪 Running {len(test_tasks)} test tasks...")
    print("-" * 50)

    results = []
    for i, task in enumerate(test_tasks, 1):
        print(f"\n📝 Task {i}: {task}")

        result = await engine.execute_with_multi_provider_retry(
            example_task_function, task, max_attempts=3
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

    # Show final statistics
    print("\n📈 Final Statistics:")
    final_stats = engine.get_provider_stats()

    print(f"  Total Requests: {final_stats['session_stats']['total_requests']}")
    print(
        f"  Success Rate: {final_stats['session_stats']['successful_requests']}/{final_stats['session_stats']['total_requests']}"
    )
    print(
        f"  Avg Response Time: {final_stats['session_stats']['avg_response_time']:.2f}s"
    )

    print("\n🏆 Provider Performance:")
    for provider, detail in final_stats["provider_details"].items():
        if detail["total_attempts"] > 0:
            print(
                f"  {provider}: {detail['success_rate']} ({detail['total_attempts']} attempts)"
            )

    return results


if __name__ == "__main__":
    asyncio.run(test_multi_provider_engine())
