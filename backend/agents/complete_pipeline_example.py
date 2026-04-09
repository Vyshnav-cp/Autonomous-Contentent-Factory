"""
Complete Content Pipeline: Research → Copywriting → Editing

Shows the full workflow from raw text to validated marketing content.
"""

from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent
from editor_agent import EditorAgent
import json


def run_content_pipeline(raw_text: str) -> dict:
    """
    Execute complete content generation and validation pipeline.

    Args:
        raw_text: Raw product description

    Returns:
        Dictionary with all results from each agent
    """

    print("=" * 70)
    print("🚀 CONTENT PIPELINE: RESEARCH → COPYWRITING → EDITING")
    print("=" * 70)

    # ============================================================================
    # STEP 1: RESEARCH AGENT - Extract product information
    # ============================================================================
    print("\n" + "=" * 70)
    print("STEP 1️⃣  : RESEARCH AGENT - Analyzing Product")
    print("=" * 70)

    researcher = ResearchAgent()
    research_result = researcher.analyze(raw_text)

    if research_result["status"] != "success":
        raise Exception("Research analysis failed")

    analysis = research_result["analysis"]
    print(f"✓ Product: {analysis['product_name']}")
    print(f"✓ Features extracted: {len(analysis['key_features'])}")
    print(f"✓ Ambiguous statements flagged: {len(analysis['ambiguous_statements'])}")
    print(f"✓ Value Proposition: {analysis['value_proposition']}")

    # ============================================================================
    # STEP 2: COPYWRITER AGENT - Generate marketing content
    # ============================================================================
    print("\n" + "=" * 70)
    print("STEP 2️⃣  : COPYWRITER AGENT - Generating Content")
    print("=" * 70)

    factsheet = {
        "product_name": analysis["product_name"],
        "key_features": analysis["key_features"],
        "technical_specs": analysis["technical_specs"],
        "target_audience": analysis["target_audience"],
        "value_proposition": analysis["value_proposition"],
    }

    copywriter = CopywriterAgent()
    content_result = copywriter.generate_content(factsheet)

    if content_result["status"] != "success":
        raise Exception("Content generation failed")

    print("✓ Blog post generated (500 words)")
    print(f"✓ Blog word count: {content_result['metadata']['blog_word_count']}")
    print("✓ Tweet thread generated (5 tweets)")
    print("✓ Email teaser generated (1 paragraph)")

    # ============================================================================
    # STEP 3: EDITOR AGENT - Validate content
    # ============================================================================
    print("\n" + "=" * 70)
    print("STEP 3️⃣  : EDITOR AGENT - Validating Content")
    print("=" * 70)

    editor = EditorAgent()
    validation_result = editor.validate_content(
        factsheet, content_result["content"]
    )

    if validation_result["status"] != "success":
        raise Exception("Content validation failed")

    validation = validation_result["validation"]
    print(f"✓ Overall Status: {validation['overall_status']}")
    print(f"✓ Confidence Score: {validation['confidence_score']}%")

    # Detailed validation scores
    print("\n📊 Validation Scores:")
    print(
        f"  - Blog Accuracy: {validation['blog_post_review'].get('accuracy_score', 'N/A')}%"
    )
    print(
        f"  - Tweet Accuracy: {validation['tweet_thread_review'].get('accuracy_score', 'N/A')}%"
    )
    print(
        f"  - Email Accuracy: {validation['email_teaser_review'].get('accuracy_score', 'N/A')}%"
    )

    # Hallucinations check
    hallucinations = validation["hallucinations_detected"]
    print(f"\n🚨 Hallucinations Detected: {len(hallucinations)}")
    if hallucinations:
        for i, h in enumerate(hallucinations[:3], 1):
            print(f"  {i}. {h}")
        if len(hallucinations) > 3:
            print(f"  ... and {len(hallucinations) - 3} more")
    else:
        print("  None - Content is accurate!")

    # Recommendations
    print(f"\n💡 Recommendations for Improvement:")
    for i, rec in enumerate(validation.get("recommendations", [])[:5], 1):
        print(f"  {i}. {rec}")

    # ============================================================================
    # FINAL RESULTS
    # ============================================================================
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE")
    print("=" * 70)

    final_result = {
        "status": "success",
        "workflow": "research_copywriting_editing",
        "steps_completed": 3,
        "research_analysis": research_result,
        "factsheet": factsheet,
        "generated_content": content_result,
        "validation_result": validation_result,
        "approval_status": validation["overall_status"],
        "confidence": validation["confidence_score"],
    }

    # Content Summary
    print("\n📋 CONTENT SUMMARY:")
    print(f"  Product: {factsheet['product_name']}")
    print(f"  Blog Length: {content_result['metadata']['blog_word_count']} words")
    print(f"  Tweets: {len(content_result['content']['tweet_thread'])}")
    print(f"  Approval: {validation['overall_status']}")

    # Quality Assessment
    print("\n⭐ QUALITY ASSESSMENT:")
    print(
        f"  Blog Quality: {validation['blog_post_review'].get('overall_quality', 'N/A')}"
    )
    print(
        f"  Tweet Quality: {validation['tweet_thread_review'].get('overall_quality', 'N/A')}"
    )
    print(
        f"  Email Quality: {validation['email_teaser_review'].get('overall_quality', 'N/A')}"
    )

    return final_result


def display_content_samples(result: dict):
    """Display sample content from the pipeline."""

    print("\n" + "=" * 70)
    print("📄 CONTENT SAMPLES")
    print("=" * 70)

    content = result["generated_content"]["content"]

    # Blog Post Sample
    print("\n📰 BLOG POST (First 400 chars):")
    print("-" * 70)
    blog = content["blog_post"]
    print(blog[:400] + "..." if len(blog) > 400 else blog)

    # Tweet Thread
    print("\n🐦 TWEET THREAD:")
    print("-" * 70)
    for i, tweet in enumerate(content["tweet_thread"], 1):
        print(f"{i}/ {tweet}")
        print(f"   ({len(tweet)} chars)")

    # Email Teaser
    print("\n📧 EMAIL TEASER:")
    print("-" * 70)
    print(content["email_teaser"])


def display_validation_details(result: dict):
    """Display detailed validation findings."""

    print("\n" + "=" * 70)
    print("🔍 VALIDATION DETAILS")
    print("=" * 70)

    validation = result["validation_result"]["validation"]

    # Blog Post Review
    blog_review = validation["blog_post_review"]
    print("\n📰 BLOG POST REVIEW:")
    print(f"  Accuracy: {blog_review.get('accuracy_score', 'N/A')}%")
    print(f"  Tone: {blog_review.get('tone_assessment', 'N/A')}")
    print(f"  Quality: {blog_review.get('overall_quality', 'N/A')}")
    print(f"  Inaccuracies: {len(blog_review.get('inaccuracies', []))}")

    # Tweet Review
    tweet_review = validation["tweet_thread_review"]
    print("\n🐦 TWEET THREAD REVIEW:")
    print(f"  Accuracy: {tweet_review.get('accuracy_score', 'N/A')}%")
    print(f"  Engagement: {tweet_review.get('engagement_score', 'N/A')}%")
    print(f"  Quality: {tweet_review.get('overall_quality', 'N/A')}")
    print(f"  Value Prop Clear: {tweet_review.get('missing_value_prop', False)}")

    # Email Review
    email_review = validation["email_teaser_review"]
    print("\n📧 EMAIL TEASER REVIEW:")
    print(f"  Accuracy: {email_review.get('accuracy_score', 'N/A')}%")
    print(f"  Persuasiveness: {email_review.get('persuasiveness', 'N/A')}%")
    print(f"  Compliance: {email_review.get('compliance_score', 'N/A')}%")
    print(f"  Quality: {email_review.get('overall_quality', 'N/A')}")


def main():
    """Execute the complete content pipeline."""

    raw_product_text = """
    DataFlow Analytics is a revolutionary enterprise-grade data pipeline platform
    that transforms how teams manage and analyze massive datasets.

    Key Features:
    - Supports 100+ data sources
    - Real-time data ingestion and streaming
    - Sub-second query performance on petabyte-scale datasets
    - Automated data quality checks
    - Advanced ML model integration
    - End-to-end encryption for data security
    - Real-time dashboards and alerts
    - Scalable infrastructure that grows with data

    Technical Specifications:
    - Processes up to 10 TB/day
    - 99.99% uptime SLA guaranteed
    - Supports SQL, Python, and Scala
    - API-first architecture
    - Cloud-native deployment on AWS, GCP, Azure
    - Global data centers with automatic failover

    Target Market:
    Enterprise data teams and organizations managing complex data ecosystems.
    Trusted by Fortune 500 companies.

    Value Proposition:
    Dramatically reduce time-to-insight and enable data-driven decision making
    with a platform built for enterprise scale and security.
    """

    try:
        # Run the complete pipeline
        result = run_content_pipeline(raw_product_text)

        # Display content samples
        display_content_samples(result)

        # Display validation details
        display_validation_details(result)

        # Display summary
        print("\n" + "=" * 70)
        print("🎉 PIPELINE EXECUTION SUMMARY")
        print("=" * 70)
        print(f"\nFinal Approval Status: {result['approval_status']}")
        print(f"Confidence Score: {result['confidence']}%")
        print(f"\nAll {result['steps_completed']} steps completed successfully!")

        # Optional: Save full result to JSON
        print("\n💾 Full result available in result dictionary")

        return result

    except Exception as e:
        print(f"\n❌ Pipeline Error: {e}")
        return None


if __name__ == "__main__":
    print("🌟 Autonomous Content Factory - Complete Pipeline Demo\n")
    result = main()

    if result and result["approval_status"] == "APPROVED":
        print(
            "\n✅ Content approved for publication!"
        )
    elif result and result["approval_status"] == "REJECTED":
        print("\n⚠️  Content rejected - review recommendations above")
    else:
        print("\n❌ Pipeline failed to complete")
