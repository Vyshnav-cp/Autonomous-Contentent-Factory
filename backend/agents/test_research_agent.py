"""
Test script for ResearchAgent.
Run this to test the agent with sample product descriptions.
"""

from research_agent import ResearchAgent
import json


def test_research_agent():
    """Test the ResearchAgent with multiple sample inputs."""

    # Test cases with different product descriptions
    test_cases = [
        {
            "name": "Cloud Storage",
            "text": """
            The CloudVault Pro is a revolutionary cloud storage solution designed for enterprises.
            It offers unlimited storage capacity with military-grade encryption. The platform supports
            real-time collaboration for teams up to 1000 members. It seamlessly integrates with
            popular productivity tools and provides AI-powered automatic file organization.
            With our advanced analytics, you'll get unprecedented insights into your data.
            Perfect for businesses looking to transform their digital infrastructure.
            Available in Standard, Professional, and Enterprise tiers.
            """,
        },
        {
            "name": "Project Management Tool",
            "text": """
            TaskMaster 360 is the most innovative project management tool ever created.
            Manage unlimited projects with our cutting-edge AI algorithms. Features include
            automated task prioritization, real-time team communication, and Gantt charts.
            Works with 50+ integrations including Slack, GitHub, and Jira. Our machine learning
            models predict project timelines with 99% accuracy. Suitable for small teams and
            large enterprises alike. Pricing starts at just $9/month with unlimited users.
            """,
        },
    ]

    try:
        agent = ResearchAgent()

        for i, test in enumerate(test_cases, 1):
            print(f"\n{'='*60}")
            print(f"Test {i}: {test['name']}")
            print(f"{'='*60}")

            result = agent.analyze(test["text"])
            print(agent.to_json(result))

            # Print a summary
            analysis = result.get("analysis", {})
            print(f"\n--- Summary ---")
            print(f"Product: {analysis.get('product_name')}")
            print(f"Features: {', '.join(analysis.get('key_features', [])[:3])}...")
            print(
                f"Ambiguous Statements: {len(analysis.get('ambiguous_statements', []))} found"
            )

    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


if __name__ == "__main__":
    success = test_research_agent()
    if success:
        print("\n✓ Tests completed successfully!")
    else:
        print("\n✗ Tests failed!")
