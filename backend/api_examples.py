"""
FastAPI Usage Examples

Demonstrates how to use the Autonomous Content Factory API.
"""

import requests
import json
from typing import Dict, List
import time


# ==================== Configuration ====================

API_BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "health": f"{API_BASE_URL}/health",
    "generate": f"{API_BASE_URL}/generate-campaign",
    "batch": f"{API_BASE_URL}/generate-campaigns-batch",
    "export": f"{API_BASE_URL}/export-campaign",
    "info": f"{API_BASE_URL}/info",
}


# ==================== Example Products ====================

EXAMPLE_PRODUCTS = {
    "cloudvault": {
        "name": "CloudVault Pro",
        "text": """
        CloudVault Pro is an enterprise cloud storage solution designed for 
        mid-market teams and organizations. Key features include unlimited 
        storage capacity, military-grade AES-256 encryption, real-time 
        collaboration capabilities, and a 99.99% uptime SLA backed by AWS 
        infrastructure. Target audience: Teams of 10-100 people. Value 
        proposition: Secure, scalable, and affordable team storage solution.
        """
    },
    "dataflow": {
        "name": "DataFlow Analytics",
        "text": """
        DataFlow Analytics is a real-time business intelligence platform that 
        transforms raw data into actionable insights. Features: automated data 
        pipeline orchestration, real-time dashboards, predictive analytics, 
        and API integration with 200+ data sources. Built on Apache Spark and 
        deployed on Kubernetes. Target: Data-driven enterprises. Value: Reduce 
        time-to-insight from weeks to minutes.
        """
    },
    "securemail": {
        "name": "SecureMail Enterprise",
        "text": """
        SecureMail Enterprise provides end-to-end encrypted communication for 
        regulated industries. HIPAA and GDPR compliant. Features: zero-knowledge 
        encryption, secure file sharing (up to 10GB), compliance audit logs, 
        and integration with Active Directory. Target: Healthcare and legal 
        professionals. Value: Enterprise-grade security without complexity.
        """
    }
}


# ==================== Helper Functions ====================

def print_section(title: str, width: int = 80):
    """Print a formatted section header"""
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}\n")


def print_response(response: requests.Response, title: str = "Response"):
    """Pretty print API response"""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body:\n{json.dumps(response.json(), indent=2)}\n")


def extract_campaign_summary(campaign: Dict) -> Dict:
    """Extract key information from campaign response"""
    data = campaign.get("data", {})
    return {
        "campaign_id": data.get("campaign_id"),
        "product_name": data.get("product_name"),
        "status": data.get("campaign_status"),
        "confidence": data.get("validation", {}).get("confidence_score"),
        "duration_seconds": data.get("duration_seconds"),
        "blog_words": len(data.get("content", {}).get("blog_post", "").split()),
        "tweets": len(data.get("content", {}).get("tweet_thread", [])),
    }


# ==================== Example 1: Health Check ====================

def example_health_check():
    """Example: Check if API is running"""
    print_section("Example 1: Health Check")
    
    try:
        response = requests.get(API_ENDPOINTS["health"])
        print_response(response, "Health Check")
        
        if response.status_code == 200:
            print("✅ API is healthy and running!")
        else:
            print("❌ API is not responding correctly")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running on localhost:8000?")
        print("   Start with: python api.py")


# ==================== Example 2: Get System Info ====================

def example_get_info():
    """Example: Get API capabilities"""
    print_section("Example 2: Get API Information")
    
    response = requests.get(API_ENDPOINTS["info"])
    info = response.json()
    
    print(f"Service: {info['service']}")
    print(f"Version: {info['version']}")
    print(f"Agents: {', '.join(info['agents'].keys())}")
    print(f"Export Formats: {', '.join(info['export_formats'])}")
    print(f"Processing Time: {info['processing_time']}")
    print(f"Cost per Campaign: {info['estimated_cost']}")
    
    print("\nAvailable Endpoints:")
    for name, details in info['endpoints'].items():
        print(f"  {details['method']:6} {details['path']:30} - {details['description']}")


# ==================== Example 3: Single Campaign Generation ====================

def example_single_campaign():
    """Example: Generate a single campaign"""
    print_section("Example 3: Single Campaign Generation")
    
    product = EXAMPLE_PRODUCTS["cloudvault"]
    
    print(f"Product: {product['name']}")
    print(f"Generating campaign...\n")
    
    start_time = time.time()
    
    response = requests.post(
        API_ENDPOINTS["generate"],
        json={
            "document_text": product["text"],
            "export_format": "json"
        }
    )
    
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        campaign = response.json()
        summary = extract_campaign_summary(campaign)
        
        print(f"✅ Campaign Generated Successfully!")
        print(f"\nCampaign ID: {summary['campaign_id']}")
        print(f"Status: {summary['status']}")
        print(f"Confidence: {summary['confidence']}%")
        print(f"Processing Time: {elapsed:.1f}s (expected: {summary['duration_seconds']:.1f}s)")
        
        # Display content summary
        print("\n📝 Content Generated:")
        print(f"  • Blog post: {summary['blog_words']} words")
        print(f"  • Tweet thread: {summary['tweets']} tweets")
        print(f"  • Email teaser: Generated")
        
        # Display first 200 chars of blog
        blog = campaign['data']['content']['blog_post']
        print(f"\n📄 Blog Preview:")
        print(f"  {blog[:200]}...\n")
        
        return campaign
    else:
        print(f"❌ Campaign generation failed: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return None


# ==================== Example 4: Batch Campaign Generation ====================

def example_batch_campaigns():
    """Example: Generate multiple campaigns"""
    print_section("Example 4: Batch Campaign Generation")
    
    products = [
        EXAMPLE_PRODUCTS["cloudvault"],
        EXAMPLE_PRODUCTS["dataflow"],
        EXAMPLE_PRODUCTS["securemail"]
    ]
    
    print(f"Generating {len(products)} campaigns...\n")
    
    start_time = time.time()
    
    response = requests.post(
        API_ENDPOINTS["batch"],
        json={
            "products": [
                {"name": p["name"], "text": p["text"]}
                for p in products
            ]
        }
    )
    
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"✅ Batch Processing Complete!")
        print(f"\nResults:")
        print(f"  Total: {result['total_campaigns']}")
        print(f"  Successful: {result['successful']} ✅")
        print(f"  Failed: {result['failed']} ❌")
        print(f"  Approval Rate: {result['summary']['approval_rate']}")
        print(f"  Total Time: {elapsed:.1f}s")
        
        # Display per-product results
        print(f"\nPer-Product Status:")
        for r in result['results']:
            status_symbol = "✅" if r['campaign_status'] == "APPROVED" else "⚠️"
            print(f"  {status_symbol} {r['product_name']}: {r['campaign_status']}")
        
        return result
    else:
        print(f"❌ Batch generation failed: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return None


# ==================== Example 5: Export Formats ====================

def example_export_formats(campaign: Dict):
    """Example: Export campaign in different formats"""
    print_section("Example 5: Export Campaign")
    
    if not campaign:
        print("⚠️  No campaign to export. Run example_single_campaign first.")
        return
    
    campaign_data = campaign['data']
    formats = ["json", "markdown", "plain"]
    
    for format_type in formats:
        print(f"\nExporting as {format_type.upper()}...")
        
        response = requests.post(
            API_ENDPOINTS["export"],
            json={
                "campaign_data": campaign_data,
                "format": format_type
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['content']
            
            # Show preview (first 300 chars)
            preview = content[:300].replace('\n', ' ') + "..."
            print(f"  ✅ Success")
            print(f"  Preview: {preview}")
            
            # Save to file
            filename = f"campaign_{campaign_data['campaign_id']}.{format_type}"
            # Note: Actual file saving would go here
            print(f"  Would save to: outputs/{filename}")
        else:
            print(f"  ❌ Export failed: {response.status_code}")


# ==================== Example 6: Error Handling ====================

def example_error_handling():
    """Example: Handle API errors"""
    print_section("Example 6: Error Handling")
    
    test_cases = [
        {
            "name": "Empty text",
            "data": {"document_text": ""}
        },
        {
            "name": "Too short text",
            "data": {"document_text": "Short text"}
        },
        {
            "name": "Invalid format",
            "data": {
                "document_text": "Valid product description..." * 10,
                "export_format": "invalid"
            }
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test['name']}")
        
        response = requests.post(
            API_ENDPOINTS["generate"],
            json=test['data']
        )
        
        if response.status_code != 200:
            error = response.json()
            print(f"  Status: {response.status_code}")
            print(f"  Error: {error.get('error', 'Unknown error')}")
            print(f"  ✓ Error handled correctly")
        else:
            print(f"  ✓ Request succeeded unexpectedly")


# ==================== Example 7: Campaign Analysis ====================

def example_campaign_analysis(campaign: Dict):
    """Example: Analyze campaign results"""
    print_section("Example 7: Campaign Analysis")
    
    if not campaign:
        print("⚠️  No campaign to analyze. Run example_single_campaign first.")
        return
    
    data = campaign['data']
    
    print("Campaign Status Summary:")
    print(f"  Campaign ID: {data['campaign_id']}")
    print(f"  Product: {data['product_name']}")
    print(f"  Overall Status: {data['campaign_status']}")
    print(f"  Confidence Score: {data['validation']['confidence_score']}%")
    
    print("\nContent Metrics:")
    blog = data['content']['blog_post']
    tweets = data['content']['tweet_thread']
    email = data['content']['email_teaser']
    print(f"  Blog: {len(blog)} characters, {len(blog.split())} words")
    print(f"  Tweets: {len(tweets)} tweets")
    for i, tweet in enumerate(tweets[:2], 1):
        print(f"    Tweet {i}: {len(tweet)} chars")
    print(f"  Email: {len(email)} characters")
    
    print("\nValidation Results:")
    validation = data['validation']
    print(f"  Approval Status: {validation['approval_status']}")
    print(f"  Hallucinations Detected: {len(validation['hallucinations_detected'])}")
    
    print("\nRecommendations:")
    for rec in data['recommendations'][:3]:
        print(f"  • {rec}")
    
    if len(data['recommendations']) > 3:
        print(f"  ... and {len(data['recommendations']) - 3} more")
    
    print("\nNext Steps:")
    for step in data['next_steps'][:3]:
        print(f"  • {step}")


# ==================== Main Demo ====================

def run_all_examples():
    """Run all examples"""
    print("\n" + "=" * 80)
    print(" Autonomous Content Factory API - Usage Examples")
    print("=" * 80)
    
    # Check if API is running
    try:
        response = requests.get(API_ENDPOINTS["health"], timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API!")
        print("   Please start the API first:")
        print("   cd backend")
        print("   python api.py")
        return
    
    # Run examples
    example_health_check()
    example_get_info()
    campaign = example_single_campaign()
    example_batch_campaigns()
    
    if campaign:
        example_export_formats(campaign)
        example_campaign_analysis(campaign)
    
    example_error_handling()
    
    print("\n" + "=" * 80)
    print(" ✅ All Examples Complete!")
    print("=" * 80 + "\n")
    
    print("Next Steps:")
    print("  1. Review API documentation: http://localhost:8000/docs")
    print("  2. Integrate into your application")
    print("  3. Deploy to production with authentication and rate limiting")
    print()


if __name__ == "__main__":
    run_all_examples()
