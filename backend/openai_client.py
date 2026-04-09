"""
OpenAI Client Wrapper

A reusable wrapper around the OpenAI API for consistent response generation
across the application.
"""

import os
from typing import Optional
from openai import OpenAI


class OpenAIClientWrapper:
    """
    A wrapper around the OpenAI client that provides a simple interface
    for generating responses using the OpenAI API.
    """

    def __init__(
        self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"
    ):
        """
        Initialize the OpenAI client wrapper.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
            model: The OpenAI model to use (default: gpt-4o-mini)

        Raises:
            ValueError: If API key is not provided and not in environment.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate a response from the OpenAI API.

        Args:
            prompt: The user prompt/message to send to the model
            temperature: Controls randomness (0.0-2.0). Lower = more focused. Default: 0.7
            max_tokens: Maximum tokens in the response. Default: None (no limit)
            system_prompt: Optional system message to set context/behavior

        Returns:
            The generated text response from the model

        Raises:
            ValueError: If prompt is empty
            Exception: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")

    def generate_response_with_context(
        self,
        prompt: str,
        context: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response with additional context.

        Args:
            prompt: The user prompt/message
            context: Additional context/background information
            temperature: Controls randomness (default: 0.7)
            max_tokens: Maximum tokens in the response

        Returns:
            The generated text response
        """
        system_prompt = f"You are a helpful assistant. Here is some context:\n\n{context}"
        return self.generate_response(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
        )

    def set_model(self, model: str) -> None:
        """
        Change the model used for generating responses.

        Args:
            model: The new model name
        """
        self.model = model

    def get_model(self) -> str:
        """
        Get the currently configured model.

        Returns:
            The current model name
        """
        return self.model


# Global instance for convenience
_default_client: Optional[OpenAIClientWrapper] = None


def get_default_client() -> OpenAIClientWrapper:
    """
    Get or create the default OpenAI client wrapper instance.

    Returns:
        The default OpenAIClientWrapper instance

    Raises:
        ValueError: If OpenAI API key is not available
    """
    global _default_client
    if _default_client is None:
        _default_client = OpenAIClientWrapper()
    return _default_client


def generate_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Convenience function to generate a response using the default client.

    Args:
        prompt: The user prompt/message to send to the model
        temperature: Controls randomness (default: 0.7)
        max_tokens: Maximum tokens in the response
        system_prompt: Optional system message for context

    Returns:
        The generated text response

    Example:
        >>> response = generate_response("What is the capital of France?")
        >>> print(response)
        "The capital of France is Paris."
    """
    client = get_default_client()
    return client.generate_response(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
    )


def main():
    """Example usage of the OpenAI client wrapper."""
    try:
        # Using the convenience function
        response = generate_response(
            prompt="Explain quantum computing in one paragraph",
            temperature=0.5,
            max_tokens=200,
        )
        print("Response:")
        print(response)
        print("\n" + "=" * 60 + "\n")

        # Using the class directly with system prompt
        client = OpenAIClientWrapper()
        response_with_context = client.generate_response(
            prompt="What are the benefits of renewable energy?",
            system_prompt="You are an environmental scientist. Be concise and informative.",
            temperature=0.6,
            max_tokens=150,
        )
        print("Response with context:")
        print(response_with_context)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
