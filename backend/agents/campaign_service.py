"""
CampaignService: Orchestrates the complete content generation workflow.

Workflow:
1. ResearchAgent: Analyzes raw product text → Factsheet
2. CopywriterAgent: Generates marketing content → Blog, Tweets, Email
3. EditorAgent: Validates content → APPROVED/REJECTED with feedback

Returns final campaign output with all results and recommendations.
"""

import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent
from editor_agent import EditorAgent


class CampaignService:
    """
    Orchestrates the complete content generation and validation workflow.
    Manages the pipeline: Research → Copywriting → Editing → Output.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        research_model: str = "gpt-4",
        copywriter_model: str = "gpt-4o-mini",
        editor_model: str = "gpt-4o-mini",
    ):
        """
        Initialize CampaignService with all agents.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
            research_model: Model for ResearchAgent (default: gpt-4)
            copywriter_model: Model for CopywriterAgent (default: gpt-4o-mini)
            editor_model: Model for EditorAgent (default: gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        # Initialize all agents
        self.research_agent = ResearchAgent(api_key=self.api_key, model=research_model)
        self.copywriter_agent = CopywriterAgent(
            api_key=self.api_key, model=copywriter_model
        )
        self.editor_agent = EditorAgent(api_key=self.api_key, model=editor_model)

        # Configuration
        self.models = {
            "research": research_model,
            "copywriter": copywriter_model,
            "editor": editor_model,
        }

    def create_campaign(self, raw_product_text: str) -> Dict[str, Any]:
        """
        Create a complete marketing campaign from raw product text.

        Orchestrates the full workflow:
        1. ResearchAgent: Extract product information
        2. CopywriterAgent: Generate marketing content
        3. EditorAgent: Validate content quality

        Args:
            raw_product_text: Raw product description text

        Returns:
            Campaign result with:
            - overall_status: SUCCESS or FAILED
            - research_analysis: Extracted product information
            - factsheet: Structured product data
            - generated_content: Blog, tweets, email
            - validation_result: Approval decision with feedback
            - campaign_status: APPROVED/REJECTED/NEEDS_REVISION
            - recommendations: Action items
            - metrics: Performance and quality metrics
        """
        if not raw_product_text or not raw_product_text.strip():
            raise ValueError("Product text cannot be empty")

        campaign_start = datetime.utcnow()
        campaign_id = self._generate_campaign_id()

        try:
            # ================================================================
            # STEP 1: Research Agent - Extract Product Information
            # ================================================================
            print("🔍 STEP 1: Analyzing product information...")
            research_result = self._run_research_phase(raw_product_text)

            if research_result["status"] != "success":
                return self._create_error_result(
                    campaign_id, "Research phase failed", campaign_start
                )

            # ================================================================
            # STEP 2: Copywriter Agent - Generate Content
            # ================================================================
            print("✍️  STEP 2: Generating marketing content...")
            factsheet = self._extract_factsheet(research_result)
            content_result = self._run_copywriting_phase(factsheet)

            if content_result["status"] != "success":
                return self._create_error_result(
                    campaign_id, "Content generation failed", campaign_start
                )

            # ================================================================
            # STEP 3: Editor Agent - Validate Content
            # ================================================================
            print("📋 STEP 3: Validating content quality...")
            validation_result = self._run_editing_phase(
                factsheet, content_result["content"]
            )

            if validation_result["status"] != "success":
                return self._create_error_result(
                    campaign_id, "Validation failed", campaign_start
                )

            # ================================================================
            # COMPILE FINAL CAMPAIGN OUTPUT
            # ================================================================
            campaign_result = self._compile_campaign_result(
                campaign_id,
                campaign_start,
                raw_product_text,
                research_result,
                factsheet,
                content_result,
                validation_result,
            )

            return campaign_result

        except Exception as e:
            return self._create_error_result(
                campaign_id, f"Campaign creation failed: {str(e)}", campaign_start
            )

    def _run_research_phase(self, raw_text: str) -> Dict[str, Any]:
        """
        Run the Research phase.

        Args:
            raw_text: Raw product description

        Returns:
            Research result
        """
        try:
            result = self.research_agent.analyze(raw_text)
            return result
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _extract_factsheet(self, research_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert research result to factsheet format.

        Args:
            research_result: Research agent output

        Returns:
            Factsheet dictionary
        """
        analysis = research_result.get("analysis", {})
        factsheet = {
            "product_name": analysis.get("product_name", "Unknown"),
            "key_features": analysis.get("key_features", []),
            "technical_specs": analysis.get("technical_specs", {}),
            "target_audience": analysis.get("target_audience", ""),
            "value_proposition": analysis.get("value_proposition", ""),
        }
        return factsheet

    def _run_copywriting_phase(self, factsheet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the Copywriting phase.

        Args:
            factsheet: Product factsheet

        Returns:
            Content generation result
        """
        try:
            result = self.copywriter_agent.generate_content(factsheet)
            return result
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _run_editing_phase(
        self, factsheet: Dict[str, Any], generated_content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run the Editing phase.

        Args:
            factsheet: Product factsheet
            generated_content: Generated marketing content

        Returns:
            Validation result
        """
        try:
            result = self.editor_agent.validate_content(factsheet, generated_content)
            return result
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _compile_campaign_result(
        self,
        campaign_id: str,
        start_time: datetime,
        raw_text: str,
        research_result: Dict[str, Any],
        factsheet: Dict[str, Any],
        content_result: Dict[str, Any],
        validation_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compile the final campaign result from all phases.

        Args:
            campaign_id: Unique campaign identifier
            start_time: Campaign start time
            raw_text: Original product text
            research_result: Research phase output
            factsheet: Extracted factsheet
            content_result: Generated content
            validation_result: Validation results

        Returns:
            Complete campaign result
        """
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()

        validation = validation_result.get("validation", {})
        approval_status = validation.get("overall_status", "UNKNOWN")

        # Determine campaign status
        campaign_status = self._determine_campaign_status(
            approval_status, validation
        )

        # Extract metrics
        metrics = self._calculate_metrics(
            research_result, content_result, validation_result, duration
        )

        # Generate recommendations
        recommendations = self._generate_campaign_recommendations(
            research_result, validation_result, campaign_status
        )

        result = {
            "status": "success",
            "campaign_id": campaign_id,
            "timestamp": end_time.isoformat(),
            "duration_seconds": duration,
            "campaign_status": campaign_status,
            "product_name": factsheet.get("product_name"),
            "phases": {
                "research": {
                    "status": research_result.get("status"),
                    "product_name": research_result.get("analysis", {}).get(
                        "product_name"
                    ),
                    "features_extracted": len(
                        research_result.get("analysis", {}).get("key_features", [])
                    ),
                    "ambiguities_found": len(
                        research_result.get("analysis", {}).get("ambiguous_statements", [])
                    ),
                },
                "copywriting": {
                    "status": content_result.get("status"),
                    "blog_words": content_result.get("metadata", {}).get(
                        "blog_word_count", 0
                    ),
                    "tweets_generated": content_result.get("metadata", {}).get(
                        "tweet_count", 0
                    ),
                },
                "editing": {
                    "status": validation_result.get("status"),
                    "overall_status": approval_status,
                    "confidence_score": validation.get("confidence_score", 0),
                    "hallucinations_detected": len(
                        validation.get("hallucinations_detected", [])
                    ),
                },
            },
            "factsheet": factsheet,
            "content": {
                "blog_post": content_result.get("content", {}).get("blog_post", ""),
                "tweet_thread": content_result.get("content", {}).get(
                    "tweet_thread", []
                ),
                "email_teaser": content_result.get("content", {}).get(
                    "email_teaser", ""
                ),
            },
            "validation": {
                "approval_status": approval_status,
                "confidence_score": validation.get("confidence_score", 0),
                "blog_review": validation.get("blog_post_review", {}),
                "tweet_review": validation.get("tweet_thread_review", {}),
                "email_review": validation.get("email_teaser_review", {}),
                "hallucinations": validation.get("hallucinations_detected", []),
                "tone_quality": validation.get("tone_quality", {}),
            },
            "metrics": metrics,
            "recommendations": recommendations,
            "next_steps": self._suggest_next_steps(campaign_status),
        }

        return result

    def _determine_campaign_status(
        self, approval_status: str, validation: Dict[str, Any]
    ) -> str:
        """
        Determine overall campaign status.

        Args:
            approval_status: Content approval status
            validation: Validation details

        Returns:
            Campaign status (APPROVED, NEEDS_REVISION, or REJECTED)
        """
        if approval_status == "APPROVED":
            return "APPROVED"
        elif approval_status == "REJECTED":
            # Check if repairable
            hallucinations = validation.get("hallucinations_detected", [])
            if len(hallucinations) <= 5:
                return "NEEDS_REVISION"
            else:
                return "REJECTED"
        else:
            return "NEEDS_REVISION"

    def _calculate_metrics(
        self,
        research_result: Dict[str, Any],
        content_result: Dict[str, Any],
        validation_result: Dict[str, Any],
        duration: float,
    ) -> Dict[str, Any]:
        """Calculate campaign metrics."""
        analysis = research_result.get("analysis", {})
        content = content_result.get("content", {})
        validation = validation_result.get("validation", {})

        metrics = {
            "processing_time": round(duration, 2),
            "research_metrics": {
                "features_extracted": len(analysis.get("key_features", [])),
                "specs_found": len(analysis.get("technical_specs", {})),
                "ambiguities_flagged": len(analysis.get("ambiguous_statements", [])),
            },
            "content_metrics": {
                "blog_word_count": len(content.get("blog_post", "").split()),
                "tweet_count": len(content.get("tweet_thread", [])),
                "email_length": len(content.get("email_teaser", "")),
            },
            "quality_metrics": {
                "blog_accuracy": validation.get("blog_post_review", {}).get(
                    "accuracy_score", 0
                ),
                "tweet_accuracy": validation.get("tweet_thread_review", {}).get(
                    "accuracy_score", 0
                ),
                "email_accuracy": validation.get("email_teaser_review", {}).get(
                    "accuracy_score", 0
                ),
                "overall_confidence": validation.get("confidence_score", 0),
            },
        }

        return metrics

    def _generate_campaign_recommendations(
        self,
        research_result: Dict[str, Any],
        validation_result: Dict[str, Any],
        campaign_status: str,
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Check for ambiguous statements
        ambiguities = (
            research_result.get("analysis", {}).get("ambiguous_statements", [])
        )
        if ambiguities:
            recommendations.append(
                f"Clarify {len(ambiguities)} ambiguous product claims before finalizing"
            )

        # Check hallucinations
        validation = validation_result.get("validation", {})
        hallucinations = validation.get("hallucinations_detected", [])
        if hallucinations:
            recommendations.append(
                f"Address {len(hallucinations)} hallucinated claims in content"
            )

        # Check quality scores
        blog_acc = (
            validation.get("blog_post_review", {}).get("accuracy_score", 100)
        )
        tweet_acc = (
            validation.get("tweet_thread_review", {}).get("accuracy_score", 100)
        )
        email_acc = (
            validation.get("email_teaser_review", {}).get("accuracy_score", 100)
        )

        if blog_acc < 80:
            recommendations.append("Improve blog post accuracy (currently <80%)")
        if tweet_acc < 80:
            recommendations.append("Improve tweet thread accuracy (currently <80%)")
        if email_acc < 80:
            recommendations.append("Improve email teaser accuracy (currently <80%)")

        # Campaign-specific recommendations
        if campaign_status == "APPROVED":
            recommendations.insert(0, "✅ Campaign approved for publication")
        elif campaign_status == "NEEDS_REVISION":
            recommendations.insert(
                0, "⚠️  Campaign needs revision before publication"
            )
        else:
            recommendations.insert(0, "❌ Campaign rejected - major revision required")

        return recommendations[:10]  # Top 10 recommendations

    def _suggest_next_steps(self, campaign_status: str) -> List[str]:
        """Suggest next steps based on campaign status."""
        if campaign_status == "APPROVED":
            return [
                "1. Review campaign output for publication readiness",
                "2. Schedule content posting across channels",
                "3. Set up email distribution",
                "4. Monitor social media engagement",
                "5. Track campaign metrics",
            ]
        elif campaign_status == "NEEDS_REVISION":
            return [
                "1. Address recommendations above",
                "2. Regenerate specific content formats if needed",
                "3. Re-run validation",
                "4. Get stakeholder review",
                "5. Update product information if inaccurate",
            ]
        else:
            return [
                "1. Review failed validation report",
                "2. Update product factsheet",
                "3. Regenerate content completely",
                "4. Re-run entire campaign",
                "5. Consider manual content creation",
            ]

    def _generate_campaign_id(self) -> str:
        """Generate unique campaign ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"CAMP-{timestamp}"

    def _create_error_result(
        self, campaign_id: str, error_msg: str, start_time: datetime
    ) -> Dict[str, Any]:
        """Create error result."""
        return {
            "status": "error",
            "campaign_id": campaign_id,
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": (datetime.utcnow() - start_time).total_seconds(),
            "error": error_msg,
            "campaign_status": "FAILED",
        }

    def create_campaign_batch(
        self, products: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Create campaigns for multiple products.

        Args:
            products: List of {"name": str, "text": str} dictionaries

        Returns:
            List of campaign results
        """
        results = []
        total = len(products)

        for i, product in enumerate(products, 1):
            try:
                print(f"\n📦 Processing campaign {i}/{total}: {product.get('name')}")
                result = self.create_campaign(product.get("text", ""))
                results.append(result)
            except Exception as e:
                results.append(
                    {
                        "status": "error",
                        "error": str(e),
                        "product_name": product.get("name"),
                        "index": i,
                    }
                )

        return results

    def to_json(self, result: Dict[str, Any]) -> str:
        """Convert result to formatted JSON string."""
        return json.dumps(result, indent=2)

    def export_campaign(
        self, result: Dict[str, Any], format: str = "json"
    ) -> str:
        """
        Export campaign in specified format.

        Args:
            result: Campaign result
            format: Export format (json, markdown, or plain)

        Returns:
            Formatted campaign output
        """
        if format == "json":
            return self.to_json(result)
        elif format == "markdown":
            return self._export_markdown(result)
        elif format == "plain":
            return self._export_plain_text(result)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_markdown(self, result: Dict[str, Any]) -> str:
        """Export campaign as Markdown."""
        output = []
        output.append(f"# Campaign: {result.get('product_name', 'Unknown')}\n")
        output.append(f"**Status**: {result.get('campaign_status', 'UNKNOWN')}\n")
        output.append(
            f"**Confidence**: {result.get('validation', {}).get('confidence_score', 0)}%\n\n"
        )

        # Content
        output.append("## Blog Post\n")
        output.append(result.get("content", {}).get("blog_post", "")[:500] + "...\n\n")

        output.append("## Tweets\n")
        for i, tweet in enumerate(result.get("content", {}).get("tweet_thread", []), 1):
            output.append(f"{i}. {tweet}\n")

        output.append("\n## Email Teaser\n")
        output.append(result.get("content", {}).get("email_teaser", "") + "\n\n")

        # Recommendations
        output.append("## Recommendations\n")
        for rec in result.get("recommendations", []):
            output.append(f"- {rec}\n")

        return "".join(output)

    def _export_plain_text(self, result: Dict[str, Any]) -> str:
        """Export campaign as plain text."""
        output = []
        output.append("=" * 70)
        output.append(f"CAMPAIGN: {result.get('product_name', 'Unknown')}")
        output.append("=" * 70)
        output.append(f"\nStatus: {result.get('campaign_status', 'UNKNOWN')}")
        output.append(
            f"Confidence: {result.get('validation', {}).get('confidence_score', 0)}%"
        )

        output.append("\n" + "-" * 70)
        output.append("BLOG POST")
        output.append("-" * 70)
        output.append(result.get("content", {}).get("blog_post", ""))

        output.append("\n" + "-" * 70)
        output.append("TWEETS")
        output.append("-" * 70)
        for i, tweet in enumerate(result.get("content", {}).get("tweet_thread", []), 1):
            output.append(f"\n{i}/ {tweet}")

        output.append("\n\n" + "-" * 70)
        output.append("EMAIL TEASER")
        output.append("-" * 70)
        output.append(result.get("content", {}).get("email_teaser", ""))

        output.append("\n\n" + "-" * 70)
        output.append("RECOMMENDATIONS")
        output.append("-" * 70)
        for rec in result.get("recommendations", []):
            output.append(f"\n• {rec}")

        return "\n".join(output)


def main():
    """Example usage of CampaignService."""

    raw_product_text = """
    CloudVault Pro is an enterprise-grade cloud storage platform designed for
    organizations that need secure, scalable data management. 
    
    Key capabilities:
    - Unlimited cloud storage capacity
    - Military-grade AES-256 encryption
    - Real-time team collaboration for up to 1000 users
    - AI-powered automatic file organization
    - Advanced analytics dashboard with real-time insights
    - Seamless integration with 50+ business tools
    
    Technical specifications:
    - Unlimited storage capacity
    - AES-256 encryption standard
    - Supports 1000+ concurrent users
    - 99.99% uptime SLA
    - Multi-region data centers
    - API-first architecture
    
    Target market: Enterprise teams and organizations seeking secure,
    collaborative cloud storage solutions.
    
    Value proposition: Secure, scalable cloud storage that enables seamless
    team collaboration while maintaining enterprise-grade security standards.
    """

    try:
        print("🚀 AUTONOMOUS CONTENT FACTORY - CAMPAIGN SERVICE")
        print("=" * 70)

        # Initialize service
        service = CampaignService()

        # Create campaign
        print("\n📊 Creating campaign...")
        campaign = service.create_campaign(raw_product_text)

        # Display results
        if campaign.get("status") == "success":
            print("\n✅ CAMPAIGN CREATED SUCCESSFULLY\n")
            print(f"Campaign ID: {campaign.get('campaign_id')}")
            print(f"Status: {campaign.get('campaign_status')}")
            print(f"Duration: {campaign.get('duration_seconds')}s")
            print(f"Confidence: {campaign.get('validation', {}).get('confidence_score')}%")

            # Show recommendations
            print("\n💡 Recommendations:")
            for rec in campaign.get("recommendations", [])[:5]:
                print(f"  {rec}")

            # Output formats
            print("\n📄 Export Formats Available:")
            print("  • JSON: Full structured output")
            print("  • Markdown: Formatted for documentation")
            print("  • Plain Text: Easy-to-read format")

            # Show sample content
            print("\n📰 BLOG POST (first 300 chars):")
            blog = campaign.get("content", {}).get("blog_post", "")
            print(blog[:300] + "...")

            print("\n🐦 TWEETS:")
            for i, tweet in enumerate(
                campaign.get("content", {}).get("tweet_thread", []), 1
            ):
                print(f"  {i}/ {tweet}")

            return campaign
        else:
            print(f"\n❌ Campaign creation failed: {campaign.get('error')}")
            return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


if __name__ == "__main__":
    main()
