"""
Test script for EditorAgent.
Tests validation of generated content against factsheets.
"""

from editor_agent import EditorAgent
import json


def test_editor_agent():
    """Test the EditorAgent with multiple scenarios."""

    test_cases = [
        {
            "name": "Valid Content (Should Pass)",
            "factsheet": {
                "product_name": "CloudVault Pro",
                "key_features": [
                    "Unlimited cloud storage",
                    "Military-grade encryption",
                    "Real-time team collaboration",
                    "AI-powered file organization",
                ],
                "technical_specs": {
                    "storage": "Unlimited",
                    "encryption": "AES-256",
                    "team_members": "Up to 1000",
                    "integrations": "50+",
                    "uptime_sla": "99.99%",
                },
                "target_audience": "Enterprise teams seeking secure cloud storage",
                "value_proposition": "Secure, scalable cloud storage enabling seamless team collaboration",
            },
            "content": {
                "blog_post": """CloudVault Pro is an enterprise-grade cloud storage solution designed for teams that require 
                security and scalability. With unlimited storage capacity, AES-256 encryption, and support for up to 1000 
                team members, CloudVault Pro delivers the features enterprises need. Real-time collaboration capabilities 
                enable teams to work together efficiently while maintaining 99.99% uptime. The platform integrates with 50+ 
                popular business tools, making it easy to incorporate into your existing workflow.""",
                "tweet_thread": [
                    "1/ Enterprise teams deserve better cloud storage.",
                    "2/ CloudVault Pro offers unlimited storage with military-grade encryption.",
                    "3/ Real-time collaboration for up to 1000 team members seamlessly.",
                    "4/ 99.99% uptime SLA means your data is always accessible.",
                    "5/ Transform your team's collaboration with CloudVault Pro.",
                ],
                "email_teaser": "Experience enterprise cloud storage with unlimited capacity, military-grade security, and seamless team collaboration.",
            },
        },
        {
            "name": "Content with Hallucinations (Should Fail)",
            "factsheet": {
                "product_name": "TaskMaster 360",
                "key_features": [
                    "Intelligent task prioritization",
                    "Real-time team communication",
                    "Gantt charts",
                    "Performance analytics",
                ],
                "technical_specs": {
                    "projects": "Unlimited",
                    "team_size": "1-10000",
                    "integrations": "Slack, GitHub, Jira",
                },
                "target_audience": "Project managers and development teams",
                "value_proposition": "Deliver projects on time with intelligent automation",
            },
            "content": {
                "blog_post": """TaskMaster 360 includes advanced AI that predicts project outcomes with 99.9% accuracy. 
                The platform automatically allocates budget and resources. It uses blockchain technology for security. 
                Includes built-in video conferencing with 4K quality. TaskMaster 360 also provides machine learning models 
                for customer behavior prediction. The system can automatically hire and manage team members. Compatible with 
                100+ enterprise systems out of the box.""",
                "tweet_thread": [
                    "1/ TaskMaster 360 now has quantum computing integration!",
                    "2/ Predict the future with our 99.9% accurate AI forecasting.",
                    "3/ Blockchain-secured task management for ultimate security.",
                    "4/ Works with 100+ enterprise systems automatically.",
                    "5/ TaskMaster 360: The complete enterprise solution.",
                ],
                "email_teaser": "TaskMaster 360 - now with AI fortune telling and automatic team hiring capabilities!",
            },
        },
    ]

    try:
        agent = EditorAgent()

        for test in test_cases:
            print(f"\n{'='*70}")
            print(f"TEST: {test['name']}")
            print(f"{'='*70}")

            result = agent.validate_content(test["factsheet"], test["content"])

            # Display results
            validation = result["validation"]
            print(f"\n📋 VALIDATION RESULT:")
            print(f"  Overall Status: {validation['overall_status']}")
            print(f"  Confidence: {validation['confidence_score']}%")

            print(f"\n📊 REVIEW SCORES:")
            print(f"  Blog Post Quality: {result['validation']['blog_post_review'].get('overall_quality', 'N/A')}")
            print(f"  Tweet Thread Quality: {result['validation']['tweet_thread_review'].get('overall_quality', 'N/A')}")
            print(f"  Email Teaser Quality: {result['validation']['email_teaser_review'].get('overall_quality', 'N/A')}")

            print(f"\n🚨 HALLUCINATIONS DETECTED: {len(validation['hallucinations_detected'])}")
            for hallucination in validation["hallucinations_detected"][:5]:
                print(f"  - {hallucination}")
            if len(validation["hallucinations_detected"]) > 5:
                print(f"  ... and {len(validation['hallucinations_detected']) - 5} more")

            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(validation.get("recommendations", [])[:5], 1):
                print(f"  {i}. {rec}")

            print(f"\n📄 FULL VALIDATION DETAILS:")
            print(f"  Blog Accuracy: {result['validation']['blog_post_review'].get('accuracy_score', 'N/A')}%")
            print(
                f"  Tweet Accuracy: {result['validation']['tweet_thread_review'].get('accuracy_score', 'N/A')}%"
            )
            print(f"  Email Accuracy: {result['validation']['email_teaser_review'].get('accuracy_score', 'N/A')}%")

    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


def test_batch_validation():
    """Test batch validation of multiple contents."""
    print(f"\n{'='*70}")
    print("BATCH VALIDATION TEST")
    print(f"{'='*70}")

    validations = [
        {
            "factsheet": {
                "product_name": "Product A",
                "key_features": ["Feature 1", "Feature 2"],
                "target_audience": "Enterprise",
                "value_proposition": "Better than competitors",
                "technical_specs": {"spec1": "value1"},
            },
            "generated_content": {
                "blog_post": "Product A has Feature 1 and Feature 2, perfect for Enterprise.",
                "tweet_thread": [
                    "1/ Product A is here",
                    "2/ With Feature 1",
                    "3/ And Feature 2",
                    "4/ For Enterprise",
                    "5/ Try it now!",
                ],
                "email_teaser": "Product A - Better than competitors.",
            },
        }
    ]

    try:
        agent = EditorAgent()
        results = agent.batch_validate(validations)

        for i, result in enumerate(results, 1):
            if result.get("status") == "success":
                print(f"\n✓ Item {i}: {result['validation']['overall_status']}")
                print(f"  Confidence: {result['validation']['confidence_score']}%")
            else:
                print(f"\n✗ Item {i}: Error - {result.get('error')}")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting EditorAgent Tests\n")

    success = test_editor_agent()
    batch_success = test_batch_validation()

    if success and batch_success:
        print("\n\n✅ All tests completed!")
    else:
        print("\n\n❌ Some tests failed!")
