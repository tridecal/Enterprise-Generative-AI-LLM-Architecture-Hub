"""Production Governance Engine: OpenTelemetry Tracing, Guardrails, and FinOps Metering."""

import logging
import time
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EnterpriseAIGovernance")

class TokenBudgetTracker(BaseModel):
    max_token_budget: int = Field(default=100000, description="Monthly allocated token ceiling")
    cost_per_1k_input: float = Field(default=0.0015, description="Input cost per 1000 tokens")
    cost_per_1k_output: float = Field(default=0.0020, description="Output cost per 1000 tokens")

class GuardrailEngine:
    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """Scan input prompts for malicious injections or policy violations."""
        forbidden_patterns = ["IGNORE ALL PREVIOUS INSTRUCTIONS", "DROP TABLE", "SYSTEM_OVERRIDE"]
        for pattern in forbidden_patterns:
            if pattern.lower() in prompt.lower():
                logger.error(f"Guardrail Violation Detected: Prompt contains blacklisted pattern '{pattern}'")
                return False
        return True

class FinOpsMeter:
    def __init__(self, budget_config: TokenBudgetTracker):
        self.config = budget_config

    def compute_execution_cost(self, prompt_tokens: int, completion_tokens: int) -> Dict[str, Any]:
        """Calculates precise execution cost for token usage."""
        input_cost = (prompt_tokens / 1000) * self.config.cost_per_1k_input
        output_cost = (completion_tokens / 1000) * self.config.cost_per_1k_output
        total_cost = input_cost + output_cost
        
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "estimated_cost_usd": round(total_cost, 6)
        }

def execute_governed_llm_call(prompt: str, prompt_tokens: int, completion_tokens: int) -> Optional[Dict[str, Any]]:
    """Executes an enterprise-governed LLM invocation cycle."""
    start_time = time.time()
    
    # 1. Guardrail Inspection
    if not GuardrailEngine.validate_prompt(prompt):
        raise ValueError("Execution blocked by security guardrail engine.")

    # 2. Compute FinOps Metrics
    meter = FinOpsMeter(budget_config=TokenBudgetTracker())
    cost_metrics = meter.compute_execution_cost(prompt_tokens, completion_tokens)
    
    latency = round(time.time() - start_time, 4)
    logger.info(f"Execution completed safely | Cost: ${cost_metrics['estimated_cost_usd']} | Latency: {latency}s")
    
    return cost_metrics