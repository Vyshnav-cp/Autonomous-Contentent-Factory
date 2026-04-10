"""
Campaign Service

Provides comprehensive campaign generation using AI agents.
Coordinates multiple agents to create blogs, social media content, emails, etc.
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import sys
import os

# Add parent directory to path to import openai_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai_client import OpenAIClientWrapper


class CampaignService:
    """
    Service for generating complete marketing campaigns using AI.
    """

    def __init__(self):
        """Initialize the campaign service with OpenAI client."""
        try:
            self.openai_client = OpenAIClientWrapper()
        except ValueError as e:
            raise ValueError(f"Failed to initialize CampaignService: {e}")

    def generate_full_campaign(
        self,
        product_name: str,
        product_description: str,
        target_audience: Optional[str] = None,
        tone: str = "professional",
        content_type: str = "full"
    ) -> Dict[str, Any]:
        """
        Generate a complete marketing campaign with all content types.

        Args:
            product_name: Name of the product
            product_description: Description of the product
            target_audience: Intended audience (optional)
            tone: Writing tone - 'professional', 'casual', or 'creative'
            content_type: 'full', 'blog_only', 'twitter_only'

        Returns:
            Dict with campaign_id, content (blog, twitter, email, etc.), and timestamp
        """
        campaign_id = str(uuid.uuid4())
        
        try:
            content = {}

            # Generate blog content
            if content_type in ["full", "blog_only"]:
                content["blog"] = self._generate_blog(
                    product_name, product_description, target_audience, tone
                )

            # Generate Twitter/X content
            if content_type in ["full", "twitter_only"]:
                content["twitter"] = self._generate_twitter(
                    product_name, product_description, tone
                )

            # Generate additional content only for full campaigns
            if content_type == "full":
                content["email"] = self._generate_email(
                    product_name, product_description, target_audience, tone
                )
                content["description"] = self._generate_product_description(
                    product_name, product_description, tone
                )

            return {
                "status": "success",
                "campaign_id": campaign_id,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "campaign_id": campaign_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def generate_quick_campaign(
        self,
        product_name: str,
        product_description: str,
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        Generate a quick campaign with essential content only.

        Args:
            product_name: Name of the product
            product_description: Description of the product
            tone: Writing tone

        Returns:
            Dict with blog and twitter content
        """
        try:
            content = {
                "blog": self._generate_blog(
                    product_name, product_description, None, tone
                ),
                "twitter": self._generate_twitter(
                    product_name, product_description, tone
                )
            }
            return content
        except Exception as e:
            raise Exception(f"Quick campaign generation failed: {e}")

    def _generate_blog(
        self,
        product_name: str,
        product_description: str,
        target_audience: Optional[str],
        tone: str
    ) -> str:
        """Generate blog content about the product."""
        prompt = f"""
        Write a compelling blog post about the following product:
        
        Product Name: {product_name}
        Description: {product_description}
        Target Audience: {target_audience or 'General audience'}
        Tone: {tone}
        
        Requirements:
        - Start with an engaging headline
        - Include 3-4 paragraphs
        - Highlight key features and benefits
        - End with a call-to-action
        - Use {tone} language
        - Make it informative and engaging
        
        Write the blog post now:
        """

        return self.openai_client.generate_response(
            prompt=prompt,
            temperature=0.7,
            max_tokens=800,
            system_prompt="You are an expert copywriter and content strategist. Write engaging, high-quality marketing content."
        )

    def _generate_twitter(
        self,
        product_name: str,
        product_description: str,
        tone: str
    ) -> list:
        """Generate multiple Twitter/X post options."""
        prompt = f"""
        Create 3 different Twitter/X posts for this product. Each post should be under 280 characters.
        
        Product Name: {product_name}
        Description: {product_description}
        Tone: {tone}
        
        Requirements:
        - Each post should be unique and engaging
        - Include relevant emojis
        - Include a call-to-action or value proposition
        - Use {tone} language
        - Make them shareable and impactful
        
        Format your response as a JSON array with 3 strings, like:
        ["post1", "post2", "post3"]
        
        Return ONLY the JSON array, nothing else.
        """

        try:
            response = self.openai_client.generate_response(
                prompt=prompt,
                temperature=0.8,
                max_tokens=300,
                system_prompt="You are a social media expert. Return only valid JSON."
            )
            
            # Parse JSON response
            tweets = json.loads(response)
            if isinstance(tweets, list):
                return tweets
            else:
                return [response]
        except json.JSONDecodeError:
            # If JSON parsing fails, return the response as a single tweet
            return [response.strip()]

    def _generate_email(
        self,
        product_name: str,
        product_description: str,
        target_audience: Optional[str],
        tone: str
    ) -> Dict[str, str]:
        """Generate email marketing content."""
        prompt = f"""
        Create a marketing email for the following product:
        
        Product Name: {product_name}
        Description: {product_description}
        Target Audience: {target_audience or 'General audience'}
        Tone: {tone}
        
        Requirements:
        - Include an engaging subject line
        - Include a greeting
        - Include a compelling body (2-3 paragraphs)
        - Include a clear call-to-action
        - Include a signature
        - Use {tone} language
        
        Format your response as JSON with keys: subject, greeting, body, cta, signature
        Return ONLY valid JSON.
        """

        try:
            response = self.openai_client.generate_response(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500,
                system_prompt="You are an expert email marketer. Return only valid JSON."
            )
            
            email = json.loads(response)
            return email
        except json.JSONDecodeError:
            return {
                "subject": f"Discover {product_name}",
                "body": response,
                "cta": "Learn More"
            }

    def _generate_product_description(
        self,
        product_name: str,
        product_description: str,
        tone: str
    ) -> str:
        """Generate a concise product description."""
        prompt = f"""
        Create a concise, engaging product description for:
        
        Product Name: {product_name}
        Current Description: {product_description}
        Tone: {tone}
        
        Requirements:
        - Keep it to 2-3 sentences
        - Be compelling and clear
        - Highlight the main benefit
        - Use {tone} language
        
        Write the product description:
        """

        return self.openai_client.generate_response(
            prompt=prompt,
            temperature=0.6,
            max_tokens=150,
            system_prompt="You are a product copywriter. Write clear, compelling descriptions."
        )

    def validate_campaign_request(
        self,
        product_name: str,
        product_description: str
    ) -> tuple[bool, Optional[str]]:
        """
        Validate campaign request parameters.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not product_name or not product_name.strip():
            return False, "product_name is required and cannot be empty"

        if not product_description or not product_description.strip():
            return False, "product_description is required and cannot be empty"

        if len(product_name) > 200:
            return False, "product_name is too long (max 200 characters)"

        if len(product_description) > 5000:
            return False, "product_description is too long (max 5000 characters)"

        return True, None


def main():
    """Test the campaign service."""
    print("Testing Campaign Service...")

    try:
        service = CampaignService()

        # Test product
        product_name = "CloudVault Pro"
        product_description = """
        CloudVault Pro is a secure cloud storage solution for enterprises.
        It offers unlimited storage, military-grade encryption, real-time collaboration,
        and integrates with 50+ productivity tools.
        """

        print("\n1. Generating full campaign...")
        result = service.generate_full_campaign(
            product_name=product_name,
            product_description=product_description,
            target_audience="Enterprise teams",
            tone="professional",
            content_type="full"
        )

        if result.get("status") == "success":
            print("✅ Campaign generated successfully!")
            print(f"Campaign ID: {result.get('campaign_id')}")
            content = result.get("content", {})
            print(f"Content types: {list(content.keys())}")
        else:
            print(f"❌ Generation failed: {result.get('error')}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
