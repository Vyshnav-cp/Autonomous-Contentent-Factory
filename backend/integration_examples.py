"""
Integration examples showing how to use the OpenAI client wrapper
with different components of the application.
"""

from openai_client import generate_response, OpenAIClientWrapper


def example_1_quick_response():
    """Example 1: Quick response generation."""
    print("=" * 60)
    print("Example 1: Quick Response Generation")
    print("=" * 60)

    try:
        response = generate_response(
            "Summarize the benefits of cloud computing in 2-3 sentences"
        )
        print(f"Response:\n{response}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def example_2_structured_extraction():
    """Example 2: Extract structured information."""
    print("=" * 60)
    print("Example 2: Structured Information Extraction")
    print("=" * 60)

    try:
        product_desc = """
        DataFlow is a real-time data pipeline tool that processes 
        millions of events per second. It supports 50+ data sources, 
        offers automatic scaling, and provides advanced analytics. 
        Perfect for data teams handling big data challenges.
        """

        response = generate_response(
            prompt=f"Extract the following as a numbered list: features, target audience, and key metrics\n\nProduct: {product_desc}",
            system_prompt="You are a product analyst. Be precise and concise.",
            temperature=0.3,
            max_tokens=200,
        )
        print(f"Extracted Information:\n{response}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def example_3_creative_content():
    """Example 3: Creative content generation."""
    print("=" * 60)
    print("Example 3: Creative Content Generation")
    print("=" * 60)

    try:
        client = OpenAIClientWrapper()
        response = client.generate_response(
            prompt="Create a catchy marketing tagline for a productivity app",
            temperature=1.2,
            max_tokens=50,
        )
        print(f"Tagline:\n{response}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def example_4_specialized_roles():
    """Example 4: Using system prompts for specialized roles."""
    print("=" * 60)
    print("Example 4: Specialized Roles (System Prompts)")
    print("=" * 60)

    roles = {
        "Expert Marketer": "You are a marketing expert. Create compelling copy.",
        "Tech Writer": "You are a technical writer. Explain clearly and thoroughly.",
        "Code Reviewer": "You are a code reviewer. Provide constructive feedback.",
    }

    prompt = "What are the best practices for API design?"

    for role, system_prompt in roles.items():
        try:
            response = generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=150,
            )
            print(f"\n{role}:")
            print(f"{response}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def example_5_batch_processing():
    """Example 5: Processing multiple prompts."""
    print("=" * 60)
    print("Example 5: Batch Processing")
    print("=" * 60)

    prompts = [
        "What is artificial intelligence?",
        "How does machine learning differ from AI?",
        "What are neural networks?",
    ]

    try:
        for i, prompt in enumerate(prompts, 1):
            response = generate_response(
                prompt=prompt,
                temperature=0.5,
                max_tokens=80,
            )
            print(f"\nQ{i}: {prompt}")
            print(f"A: {response}")
    except Exception as e:
        print(f"Error: {e}\n")


def example_6_controlled_output():
    """Example 6: Controlling output characteristics."""
    print("=" * 60)
    print("Example 6: Output Control (Temperature & Max Tokens)")
    print("=" * 60)

    prompt = "Write a sentence about the future of technology"

    print("\nFocused (Temperature: 0.2):")
    try:
        response = generate_response(
            prompt=prompt,
            temperature=0.2,
            max_tokens=50,
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")

    print("\nBalanced (Temperature: 0.7):")
    try:
        response = generate_response(
            prompt=prompt,
            temperature=0.7,
            max_tokens=50,
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")

    print("\nCreative (Temperature: 1.5):")
    try:
        response = generate_response(
            prompt=prompt,
            temperature=1.5,
            max_tokens=50,
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}\n")


def example_7_error_handling():
    """Example 7: Error handling and validation."""
    print("=" * 60)
    print("Example 7: Error Handling")
    print("=" * 60)

    test_cases = [
        ("", "Empty prompt"),
        ("   ", "Whitespace only"),
        ("Valid prompt", "Valid"),
    ]

    for prompt, description in test_cases:
        try:
            response = generate_response(prompt=prompt, max_tokens=50)
            print(f"✓ {description}: Success")
        except ValueError as e:
            print(f"✓ {description}: Caught error - {e}")
        except Exception as e:
            print(f"✗ {description}: Unexpected error - {e}\n")


def run_all_examples():
    """Run all examples."""
    print("\n")
    print("█" * 60)
    print("OpenAI Client Wrapper - Integration Examples")
    print("█" * 60)
    print("\n")

    examples = [
        example_1_quick_response,
        example_2_structured_extraction,
        example_3_creative_content,
        example_4_specialized_roles,
        example_5_batch_processing,
        example_6_controlled_output,
        example_7_error_handling,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Example failed: {e}\n")

    print("█" * 60)
    print("Examples completed!")
    print("█" * 60)


if __name__ == "__main__":
    run_all_examples()
