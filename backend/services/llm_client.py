"""
Multi-LLM client supporting Anthropic, OpenAI, and Mixtral
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import anthropic
import openai
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import settings


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Generate a response from the LLM"""
        pass

    @abstractmethod
    def generate_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Synchronous generation"""
        pass


class AnthropicClient(LLMClient):
    """Anthropic Claude client"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API key not found")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Async generation with Claude"""
        async_client = anthropic.AsyncAnthropic(api_key=self.api_key)

        kwargs = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        if tools:
            kwargs["tools"] = tools

        response = await async_client.messages.create(**kwargs)

        return {
            "content": response.content[0].text if response.content else "",
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "raw_response": response
        }

    def generate_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Synchronous generation with Claude"""
        kwargs = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        if tools:
            kwargs["tools"] = tools

        response = self.client.messages.create(**kwargs)

        return {
            "content": response.content[0].text if response.content else "",
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "raw_response": response
        }


class OpenAIClient(LLMClient):
    """OpenAI GPT client"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
        self.client = openai.OpenAI(api_key=self.api_key)

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Async generation with GPT"""
        async_client = openai.AsyncOpenAI(api_key=self.api_key)

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        kwargs = {
            "model": "gpt-4-turbo-preview",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if tools:
            kwargs["tools"] = tools

        response = await async_client.chat.completions.create(**kwargs)

        return {
            "content": response.choices[0].message.content or "",
            "stop_reason": response.choices[0].finish_reason,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            },
            "raw_response": response
        }

    def generate_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Synchronous generation with GPT"""
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        kwargs = {
            "model": "gpt-4-turbo-preview",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)

        return {
            "content": response.choices[0].message.content or "",
            "stop_reason": response.choices[0].finish_reason,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            },
            "raw_response": response
        }


class MixtralClient(LLMClient):
    """Mixtral client (via OpenAI-compatible API)"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.MIXTRAL_API_KEY
        if not self.api_key:
            raise ValueError("Mixtral API key not found")
        # Using OpenAI client with custom base URL for Mixtral
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.together.xyz/v1"  # Together AI for Mixtral
        )

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Async generation with Mixtral"""
        async_client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.together.xyz/v1"
        )

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        kwargs = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = await async_client.chat.completions.create(**kwargs)

        return {
            "content": response.choices[0].message.content or "",
            "stop_reason": response.choices[0].finish_reason,
            "usage": {
                "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                "output_tokens": response.usage.completion_tokens if response.usage else 0
            },
            "raw_response": response
        }

    def generate_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Synchronous generation with Mixtral"""
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        kwargs = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = self.client.chat.completions.create(**kwargs)

        return {
            "content": response.choices[0].message.content or "",
            "stop_reason": response.choices[0].finish_reason,
            "usage": {
                "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                "output_tokens": response.usage.completion_tokens if response.usage else 0
            },
            "raw_response": response
        }


class LLMFactory:
    """Factory for creating LLM clients"""

    @staticmethod
    def create_client(provider: str = None) -> LLMClient:
        """Create an LLM client based on provider"""
        provider = provider or settings.DEFAULT_LLM

        if provider == "anthropic":
            return AnthropicClient()
        elif provider == "openai":
            return OpenAIClient()
        elif provider == "mixtral":
            return MixtralClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def get_available_providers() -> List[str]:
        """Get list of available LLM providers"""
        providers = []
        if settings.ANTHROPIC_API_KEY:
            providers.append("anthropic")
        if settings.OPENAI_API_KEY:
            providers.append("openai")
        if settings.MIXTRAL_API_KEY:
            providers.append("mixtral")
        return providers
