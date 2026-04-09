"""
Test cases for the OpenAI client wrapper.
"""

from openai_client import OpenAIClientWrapper, generate_response


def test_generate_response():
    """Test the basic generate_response function."""
    try:
        response = generate_response(
            prompt="Say 'Hello World' in exactly 3 words.",
            temperature=0.3,
            max_tokens=20,
        )
        print("✓ Test 1: Basic generate_response")
        print(f"  Response: {response}\n")
        return True
    except Exception as e:
        print(f"✗ Test 1 failed: {e}\n")
        return False


def test_client_class():
    """Test the OpenAIClientWrapper class directly."""
    try:
        client = OpenAIClientWrapper()
        response = client.generate_response(
            prompt="List 3 programming languages", max_tokens=50
        )
        print("✓ Test 2: OpenAIClientWrapper class")
        print(f"  Response: {response}\n")
        return True
    except Exception as e:
        print(f"✗ Test 2 failed: {e}\n")
        return False


def test_system_prompt():
    """Test with custom system prompt."""
    try:
        client = OpenAIClientWrapper()
        response = client.generate_response(
            prompt="What is AI?",
            system_prompt="You are a helpful tech expert. Keep your answer under 50 words.",
            temperature=0.5,
            max_tokens=100,
        )
        print("✓ Test 3: With system prompt")
        print(f"  Response: {response}\n")
        return True
    except Exception as e:
        print(f"✗ Test 3 failed: {e}\n")
        return False


def test_model_switching():
    """Test model switching."""
    try:
        client = OpenAIClientWrapper()
        print(f"✓ Test 4: Model switching")
        print(f"  Initial model: {client.get_model()}")
        client.set_model("gpt-4")
        print(f"  After switch: {client.get_model()}\n")
        return True
    except Exception as e:
        print(f"✗ Test 4 failed: {e}\n")
        return False


def test_empty_prompt_error():
    """Test error handling for empty prompt."""
    try:
        client = OpenAIClientWrapper()
        response = client.generate_response(prompt="")
        print(f"✗ Test 5 failed: Should have raised ValueError\n")
        return False
    except ValueError as e:
        print(f"✓ Test 5: Empty prompt error handling")
        print(f"  Correctly caught error: {e}\n")
        return True
    except Exception as e:
        print(f"✗ Test 5 failed with unexpected error: {e}\n")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("OpenAI Client Wrapper Tests")
    print("=" * 60 + "\n")

    tests = [
        test_generate_response,
        test_client_class,
        test_system_prompt,
        test_model_switching,
        test_empty_prompt_error,
    ]

    results = []
    for test in tests:
        results.append(test())

    print("=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)

    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
