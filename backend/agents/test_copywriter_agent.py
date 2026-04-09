"""
Test script for CopywriterAgent.
Tests content generation from factsheets with various product types.
"""

from copywriter_agent import CopywriterAgent
import json


def test_copywriter_agent():
    """Test the CopywriterAgent with multiple factsheets."""

    factsheets = [
        {
            "product_name": "CloudVault Pro",
            "key_features": [
                "Unlimited cloud storage",
                "Military-grade encryption",
                "Real-time team collaboration",
                "AI-powered file organization",
                "Advanced analytics dashboard",
            ],
            "technical_specs": {
                "storage": "Unlimited",
                "encryption": "AES-256",
                "team_members": "Up to 1000",
                "integrations": "50+",
                "uptime_sla": "99.99%",
            },
            "target_audience": "Enterprise teams and businesses looking for secure, scalable cloud storage",
            "value_proposition": "Secure, scalable cloud storage that enables seamless team collaboration while protecting your most sensitive data",
        },
        {
            "product_name": "TaskMaster 360",
            "key_features": [
                "Intelligent task prioritization",
                "Real-time team communication",
                "Gantt charts and timeline visualization",
                "Automated workflow management",
                "Performance analytics",
            ],
            "technical_specs": {
                "supported_projects": "Unlimited",
                "team_size": "1-10,000 members",
                "integrations": "Slack, GitHub, Jira, Asana",
                "api_rate_limit": "10,000 requests/hour",
                "data_centers": "Global (3 regions)",
            },
            "target_audience": "Project managers, development teams, and organizations seeking streamlined project execution",
            "value_proposition": "Simplify project management with intelligent automation that gets your team on the same page and delivers projects on time",
        },
    ]

    try:
        agent = CopywriterAgent()

        for i, factsheet in enumerate(factsheets, 1):
            print(f"\n{'='*70}")
            print(f"Test {i}: {factsheet['product_name']}")
            print(f"{'='*70}")

            result = agent.generate_content(factsheet)

            # Print formatted output
            print("\n📰 BLOG POST (500 words):")
            print("-" * 70)
            print(result["content"]["blog_post"][:500] + "...")
            print(f"(Word count: {result['metadata']['blog_word_count']})")

            print("\n🐦 TWEET THREAD (5 tweets):")
            print("-" * 70)
            for j, tweet in enumerate(result["content"]["tweet_thread"], 1):
                print(f"{j}/ {tweet}")

            print("\n📧 EMAIL TEASER:")
            print("-" * 70)
            print(result["content"]["email_teaser"])

            print("\n📊 METADATA:")
            print("-" * 70)
            print(json.dumps(result["metadata"], indent=2))

    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


def test_validation():
    """Test input validation."""
    print("\n" + "=" * 70)
    print("VALIDATION TESTS")
    print("=" * 70)

    agent = CopywriterAgent()

    # Test missing required fields
    invalid_factsheets = [
        {
            "product_name": "Incomplete Product",
            # Missing key_features, target_audience, value_proposition
        },
        {
            "product_name": "Another Product",
            "key_features": "not a list",  # Wrong type
            "target_audience": "Everyone",
            "value_proposition": "Good stuff",
        },
    ]

    for i, factsheet in enumerate(invalid_factsheets, 1):
        print(f"\nTest {i}: Validating incomplete factsheet...")
        try:
            result = agent.generate_content(factsheet)
            print("  ✗ Should have raised an error")
        except ValueError as e:
            print(f"  ✓ Correctly raised ValueError: {e}")


if __name__ == "__main__":
    print("🚀 Starting CopywriterAgent Tests\n")

    success = test_copywriter_agent()
    test_validation()

    if success:
        print("\n\n✅ All content generation tests completed!")
    else:
        print("\n\n❌ Some tests failed!")
