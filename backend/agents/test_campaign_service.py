"""
Test suite for CampaignService.
Tests the complete workflow orchestration.
"""

from campaign_service import CampaignService
import json


def test_single_campaign():
    """Test creating a single campaign."""
    print("\n" + "=" * 70)
    print("TEST 1: Single Campaign Creation")
    print("=" * 70)

    product_text = """
    DataFlow Analytics is a revolutionary enterprise data pipeline platform
    that transforms how organizations manage and analyze big data.
    
    Key features:
    - Real-time data ingestion from 100+ sources
    - Sub-second query performance on petabyte-scale datasets
    - Automated data quality checks
    - Machine learning model integration
    - End-to-end encryption
    - Advanced analytics dashboards
    - Global scalability
    
    Technical specs:
    - Processes up to 10TB/day
    - 99.99% uptime SLA
    - Supports SQL, Python, Scala
    - Cloud-native architecture
    - Multi-region deployment
    
    Target: Enterprise data teams and analytics organizations
    Value: Dramatically reduce time-to-insight with enterprise-scale data platform
    """

    try:
        service = CampaignService()
        print("\n🚀 Creating campaign...")
        campaign = service.create_campaign(product_text)

        if campaign.get("status") == "success":
            print("✅ Campaign created successfully")
            print(f"   Campaign ID: {campaign.get('campaign_id')}")
            print(f"   Status: {campaign.get('campaign_status')}")
            print(f"   Confidence: {campaign.get('validation', {}).get('confidence_score')}%")
            print(f"   Duration: {campaign.get('duration_seconds')}s")

            # Show metrics
            metrics = campaign.get("metrics", {})
            print(f"\n📊 Metrics:")
            print(f"   Features extracted: {metrics.get('research_metrics', {}).get('features_extracted')}")
            print(
                f"   Blog word count: {metrics.get('content_metrics', {}).get('blog_word_count')}"
            )
            print(
                f"   Blog accuracy: {metrics.get('quality_metrics', {}).get('blog_accuracy')}%"
            )

            # Show content sample
            print(f"\n📝 Content Generated:")
            print(f"   Blog post: {len(campaign.get('content', {}).get('blog_post', ''))} chars")
            print(f"   Tweets: {len(campaign.get('content', {}).get('tweet_thread', []))} tweets")
            print(f"   Email: {len(campaign.get('content', {}).get('email_teaser', ''))} chars")

            return True
        else:
            print(f"❌ Campaign failed: {campaign.get('error')}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_batch_campaigns():
    """Test creating multiple campaigns."""
    print("\n" + "=" * 70)
    print("TEST 2: Batch Campaign Creation")
    print("=" * 70)

    products = [
        {
            "name": "CloudVault Pro",
            "text": """CloudVault Pro is a secure cloud storage solution with unlimited capacity,
                    military-grade encryption, and real-time collaboration for enterprise teams.""",
        },
        {
            "name": "TaskMaster 360",
            "text": """TaskMaster 360 is a project management platform featuring intelligent task
                    prioritization, team communication, and performance analytics for development teams.""",
        },
    ]

    try:
        service = CampaignService()
        print(f"\n🚀 Creating {len(products)} campaigns...")
        results = service.create_campaign_batch(products)

        print(f"\n📊 Batch Results:")
        for i, result in enumerate(results, 1):
            if result.get("status") == "success":
                print(
                    f"  {i}. ✅ {result.get('product_name')}: {result.get('campaign_status')}"
                )
            else:
                print(f"  {i}. ❌ Error: {result.get('error')}")

        return len([r for r in results if r.get("status") == "success"]) == len(
            products
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_export_formats():
    """Test different export formats."""
    print("\n" + "=" * 70)
    print("TEST 3: Export Formats")
    print("=" * 70)

    product_text = """
    AIAssistant Pro is an advanced AI-powered assistant designed for enterprises.
    Features: Natural language processing, multi-language support, custom training.
    Target: Large enterprises needing intelligent automation.
    Value: Automate complex workflows with AI intelligence.
    """

    try:
        service = CampaignService()
        campaign = service.create_campaign(product_text)

        if campaign.get("status") != "success":
            print("❌ Campaign creation failed")
            return False

        # Test JSON export
        print("\n📄 JSON Export:")
        json_export = service.export_campaign(campaign, format="json")
        print(f"   Generated: {len(json_export)} bytes")
        print(f"   Valid JSON: {json.loads(json_export) is not None}")

        # Test Markdown export
        print("\n📝 Markdown Export:")
        md_export = service.export_campaign(campaign, format="markdown")
        print(f"   Generated: {len(md_export)} bytes")
        print(f"   Contains blog: {'Blog Post' in md_export}")
        print(f"   Contains tweets: {'Tweets' in md_export}")

        # Test plain text export
        print("\n📋 Plain Text Export:")
        txt_export = service.export_campaign(campaign, format="plain")
        print(f"   Generated: {len(txt_export)} bytes")
        print(f"   Contains campaign: {'CAMPAIGN' in txt_export}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_campaign_phases():
    """Test individual campaign phases."""
    print("\n" + "=" * 70)
    print("TEST 4: Campaign Phases Breakdown")
    print("=" * 70)

    product_text = """
    SecureVault is an enterprise security platform.
    Features: Encryption, access control, audit logging.
    Target: Enterprise security teams.
    Value: Enterprise-grade security infrastructure.
    """

    try:
        service = CampaignService()
        campaign = service.create_campaign(product_text)

        if campaign.get("status") != "success":
            print("❌ Campaign creation failed")
            return False

        phases = campaign.get("phases", {})

        print("\n🔍 Research Phase:")
        print(f"   Status: {phases.get('research', {}).get('status')}")
        print(f"   Features extracted: {phases.get('research', {}).get('features_extracted')}")
        print(f"   Ambiguities found: {phases.get('research', {}).get('ambiguities_found')}")

        print("\n✍️  Copywriting Phase:")
        print(f"   Status: {phases.get('copywriting', {}).get('status')}")
        print(f"   Blog words: {phases.get('copywriting', {}).get('blog_words')}")
        print(f"   Tweets: {phases.get('copywriting', {}).get('tweets_generated')}")

        print("\n📋 Editing Phase:")
        print(f"   Status: {phases.get('editing', {}).get('status')}")
        print(f"   Approval: {phases.get('editing', {}).get('overall_status')}")
        print(
            f"   Confidence: {phases.get('editing', {}).get('confidence_score')}%"
        )
        print(
            f"   Hallucinations: {phases.get('editing', {}).get('hallucinations_detected')}"
        )

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_error_handling():
    """Test error handling."""
    print("\n" + "=" * 70)
    print("TEST 5: Error Handling")
    print("=" * 70)

    try:
        service = CampaignService()

        # Test empty text
        print("\n  Test: Empty product text")
        try:
            service.create_campaign("")
            print("  ❌ Should have raised error for empty text")
            return False
        except ValueError as e:
            print(f"  ✅ Correctly raised error: {str(e)[:50]}...")

        print("\n✅ Error handling tests passed")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting CampaignService Tests\n")

    tests = [
        ("Single Campaign", test_single_campaign),
        ("Batch Campaigns", test_batch_campaigns),
        ("Export Formats", test_export_formats),
        ("Campaign Phases", test_campaign_phases),
        ("Error Handling", test_error_handling),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
