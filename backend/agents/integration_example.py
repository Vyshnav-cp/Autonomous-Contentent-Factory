"""
Integration example showing ResearchAgent → CopywriterAgent workflow.

Workflow:
1. ResearchAgent analyzes raw product text
2. Extract structured data (factsheet)
3. CopywriterAgent generates marketing content from factsheet
"""

from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent
import json


def extract_and_generate_content(raw_text: str) -> dict:
    """
    Complete workflow: analyze raw text → generate marketing content.

    Args:
        raw_text: Raw product description

    Returns:
        Dictionary with analysis results and generated content
    """
    print("=" * 70)
    print("🔍 STEP 1: Analyzing Raw Product Text")
    print("=" * 70)

    # Step 1: Extract product information
    researcher = ResearchAgent()
    research_result = researcher.analyze(raw_text)

    if research_result["status"] != "success":
        raise Exception("Research analysis failed")

    analysis = research_result["analysis"]
    print(f"✓ Product identified: {analysis['product_name']}")
    print(f"✓ Extracted {len(analysis['key_features'])} features")
    print(f"✓ Identified {len(analysis['ambiguous_statements'])} ambiguous statements")

    # Step 2: Convert analysis to factsheet format for copywriter
    print("\n" + "=" * 70)
    print("📋 STEP 2: Creating Factsheet")
    print("=" * 70)

    factsheet = {
        "product_name": analysis["product_name"],
        "key_features": analysis["key_features"],
        "technical_specs": analysis["technical_specs"],
        "target_audience": analysis["target_audience"],
        "value_proposition": analysis["value_proposition"],
    }

    print("✓ Factsheet created with:")
    print(f"  - Product: {factsheet['product_name']}")
    print(f"  - Features: {len(factsheet['key_features'])}")
    print(f"  - Specs: {len(factsheet['technical_specs'])} items")
    print(f"  - Value Prop: {factsheet['value_proposition'][:50]}...")

    # Step 3: Generate marketing content
    print("\n" + "=" * 70)
    print("✍️  STEP 3: Generating Marketing Content")
    print("=" * 70)

    copywriter = CopywriterAgent()
    content_result = copywriter.generate_content(factsheet)

    if content_result["status"] != "success":
        raise Exception("Content generation failed")

    print("✓ Blog post generated")
    print("✓ Tweet thread generated (5 tweets)")
    print("✓ Email teaser generated")

    # Compile complete result
    complete_result = {
        "status": "success",
        "workflow": "research_to_copywriting",
        "research_analysis": research_result,
        "factsheet": factsheet,
        "generated_content": content_result,
    }

    return complete_result


def main():
    """Run the integration example."""

    raw_product_text = """
    Introducing DataFlow Analytics - the enterprise-grade data pipeline platform 
    that transforms how teams manage and analyze data at scale.
    
    DataFlow Analytics is built for data engineers and analysts who need to process 
    massive datasets quickly and reliably. Our platform features automated data ingestion, 
    real-time streaming capabilities, and advanced transformation tools.
    
    Key capabilities include:
    - Support for 100+ data sources
    - Sub-second query performance on petabyte-scale datasets
    - Machine learning model integration
    - Automated data quality checks
    - Real-time dashboards and alerts
    - Advanced security with end-to-end encryption
    - Scalable infrastructure that grows with your data
    
    Technical specifications:
    - Processes up to 10 TB/day
    - 99.99% uptime SLA
    - Supports SQL, Python, and Scala
    - API-first architecture
    - Cloud-native deployment (AWS, GCP, Azure)
    
    Perfect for enterprises managing complex data ecosystems. Trusted by Fortune 500 companies.
    Dramatically reduces time-to-insight and enables data-driven decision making.
    """

    try:
        result = extract_and_generate_content(raw_product_text)

        # Display results
        print("\n" + "=" * 70)
        print("📊 RESULTS SUMMARY")
        print("=" * 70)

        content = result["generated_content"]["content"]

        print("\n📰 BLOG POST (first 300 chars):")
        print("-" * 70)
        print(content["blog_post"][:300] + "...")
        print(f"(Total: {result['generated_content']['metadata']['blog_word_count']} words)")

        print("\n🐦 TWEET THREAD:")
        print("-" * 70)
        for i, tweet in enumerate(content["tweet_thread"], 1):
            char_count = len(tweet)
            print(f"{i}/ {tweet} ({char_count} chars)")

        print("\n📧 EMAIL TEASER:")
        print("-" * 70)
        print(content["email_teaser"])

        # Display full JSON for reference
        print("\n" + "=" * 70)
        print("📄 FULL RESULT (JSON)")
        print("=" * 70)
        print(json.dumps(result, indent=2)[:1000] + "...\n[Truncated for readability]")

        print("\n" + "=" * 70)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

    return True


if __name__ == "__main__":
    main()
