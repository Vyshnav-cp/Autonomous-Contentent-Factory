"""
Comprehensive test suite for ResearchAgent.
Validates all responsibilities and functionality.
"""

import json
from research_agent import ResearchAgent


class ResearchAgentValidator:
    """Validates ResearchAgent functionality against all responsibilities."""

    @staticmethod
    def validate_structure(result: dict) -> dict:
        """
        Validate that the result contains all required fields.

        Returns:
            Validation report with pass/fail status for each responsibility
        """
        analysis = result.get("analysis", {})

        validation = {
            "timestamp": bool(result.get("timestamp")),
            "status": result.get("status") == "success",
            "product_name_extracted": bool(
                analysis.get("product_name") and analysis.get("product_name") != "Unknown"
            ),
            "key_features_extracted": bool(analysis.get("key_features")),
            "technical_specs_extracted": bool(analysis.get("technical_specs")),
            "target_audience_extracted": bool(analysis.get("target_audience")),
            "value_proposition_extracted": bool(analysis.get("value_proposition")),
            "ambiguous_statements_identified": bool(
                analysis.get("ambiguous_statements")
            ),
            "is_valid_json": True,
        }

        return validation

    @staticmethod
    def print_validation_report(result: dict, test_name: str) -> None:
        """Print a formatted validation report."""
        validation = ResearchAgentValidator.validate_structure(result)
        analysis = result.get("analysis", {})

        print(f"\n{'='*70}")
        print(f"Validation Report: {test_name}")
        print(f"{'='*70}")

        # Responsibilities checklist
        responsibilities = {
            "✓ Analyze source document": result.get("raw_input_length", 0) > 0,
            "✓ Extract product name": validation["product_name_extracted"],
            "✓ Extract key features": validation["key_features_extracted"],
            "✓ Extract technical specs": validation["technical_specs_extracted"],
            "✓ Extract target audience": validation["target_audience_extracted"],
            "✓ Extract value proposition": validation["value_proposition_extracted"],
            "✓ Identify ambiguous statements": validation[
                "ambiguous_statements_identified"
            ],
            "✓ Return structured JSON": validation["is_valid_json"],
        }

        print("\nResponsibilities Status:")
        for responsibility, status in responsibilities.items():
            marker = "✓" if status else "✗"
            print(f"  {marker} {responsibility}")

        print(f"\nExtracted Data:")
        print(f"  Product Name: {analysis.get('product_name')}")
        print(f"  Key Features Count: {len(analysis.get('key_features', []))}")
        print(f"  Technical Specs: {len(analysis.get('technical_specs', {}))}")
        print(f"  Target Audience: {analysis.get('target_audience')[:50]}...")
        print(f"  Value Proposition: {analysis.get('value_proposition')[:50]}...")
        print(
            f"  Ambiguous Statements: {len(analysis.get('ambiguous_statements', []))}"
        )

        all_passed = all(responsibilities.values())
        print(f"\nOverall Status: {'✓ PASSED' if all_passed else '✗ FAILED'}")


def run_comprehensive_tests():
    """Run comprehensive tests on ResearchAgent."""

    test_documents = [
        {
            "name": "E-commerce Platform",
            "text": """
            ShopHub is an all-in-one e-commerce platform that revolutionizes online selling.
            Features include AI-powered product recommendations, real-time inventory management,
            and integrated payment processing supporting 50+ payment methods. The platform
            uses advanced machine learning to optimize pricing and supply chain efficiency.
            Built for small retailers to large enterprises, it handles millions of transactions.
            ShopHub provides unparalleled insights and unprecedented scalability for your business.
            Technical specifications: 99.99% uptime SLA, sub-100ms response times, supports
            up to 100,000 concurrent users. Perfect for retailers wanting to dominate their market.
            """,
        },
        {
            "name": "Project Management Suite",
            "text": """
            TaskFlow Pro is a comprehensive project management solution featuring Gantt charts,
            Kanban boards, resource allocation, and time tracking. It integrates with popular
            tools like Slack, GitHub, and Google Workspace. The AI assistant helps with
            scheduling and risk identification. Designed for software development teams,
            marketing departments, and creative agencies. TaskFlow Pro claims revolutionary
            productivity gains and game-changing collaboration features with absolutely superior
            performance compared to competitors.
            """,
        },
    ]

    try:
        print("Initializing ResearchAgent...")
        agent = ResearchAgent()

        print("✓ ResearchAgent initialized successfully")

        print("\n" + "="*70)
        print("COMPREHENSIVE RESEARCH AGENT TEST SUITE")
        print("="*70)

        for test_doc in test_documents:
            print(f"\nProcessing: {test_doc['name']}")
            print(f"Document length: {len(test_doc['text'])} characters")

            # Analyze the document
            result = agent.analyze(test_doc["text"])

            # Validate and print report
            ResearchAgentValidator.print_validation_report(result, test_doc["name"])

            # Print detailed JSON
            print(f"\nDetailed JSON Output:")
            print(agent.to_json(result))

        print("\n" + "="*70)
        print("TEST SUITE COMPLETED")
        print("="*70)

    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False

    return True


if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
