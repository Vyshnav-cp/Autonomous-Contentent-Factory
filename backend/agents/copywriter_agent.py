"""
CopywriterAgent: Generates professional marketing content from product factsheets.

Responsibilities:
- Accept factsheet JSON input
- Generate 500-word blog post (professional tone)
- Generate 5-tweet thread (engaging tone)
- Generate email teaser paragraph
- Highlight value proposition throughout
"""

import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
from openai import OpenAI


class CopywriterAgent:
    """
    An AI agent that generates diverse marketing content from product factsheets.
    Creates blog posts, tweet threads, and email teasers with consistent value proposition messaging.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the CopywriterAgent with OpenAI client.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
            model: The OpenAI model to use (default: gpt-4o-mini for cost-efficiency)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_content(self, factsheet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate all marketing content from a factsheet.

        Args:
            factsheet: Dictionary containing product information with keys:
                      - product_name (str): Name of the product
                      - key_features (list): List of main features
                      - technical_specs (dict): Technical specifications
                      - target_audience (str): Intended audience
                      - value_proposition (str): Core value offered
                      - ambiguous_statements (list): Optional, statements to avoid

        Returns:
            Dictionary containing:
            - blog_post: 500-word professional blog post
            - tweet_thread: List of 5 tweets
            - email_teaser: One paragraph email teaser
            - metadata: Generation metadata
        """
        self._validate_factsheet(factsheet)

        try:
            blog_post = self._generate_blog_post(factsheet)
            tweet_thread = self._generate_tweet_thread(factsheet)
            email_teaser = self._generate_email_teaser(factsheet)

            result = {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "product_name": factsheet.get("product_name"),
                "content": {
                    "blog_post": blog_post,
                    "tweet_thread": tweet_thread,
                    "email_teaser": email_teaser,
                },
                "metadata": {
                    "model_used": self.model,
                    "blog_word_count": len(blog_post.split()),
                    "tweet_count": len(tweet_thread),
                    "value_proposition": factsheet.get("value_proposition", ""),
                },
            }

            return result

        except Exception as e:
            raise Exception(f"Error generating content: {e}")

    def _validate_factsheet(self, factsheet: Dict[str, Any]) -> None:
        """
        Validate that factsheet contains required fields.

        Args:
            factsheet: Dictionary to validate

        Raises:
            ValueError: If required fields are missing
        """
        required_fields = [
            "product_name",
            "key_features",
            "target_audience",
            "value_proposition",
        ]

        missing_fields = [field for field in required_fields if field not in factsheet]
        if missing_fields:
            raise ValueError(
                f"Factsheet missing required fields: {', '.join(missing_fields)}"
            )

        if not isinstance(factsheet.get("key_features"), list):
            raise ValueError("key_features must be a list")

        if not factsheet.get("product_name"):
            raise ValueError("product_name cannot be empty")

        if not factsheet.get("value_proposition"):
            raise ValueError("value_proposition cannot be empty")

    def _generate_blog_post(self, factsheet: Dict[str, Any]) -> str:
        """
        Generate a 500-word professional blog post.

        Args:
            factsheet: Product factsheet dictionary

        Returns:
            Blog post text (approximately 500 words)
        """
        prompt = self._build_blog_prompt(factsheet)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical writer and marketing professional. Write engaging, informative blog posts that highlight product benefits and value. Use clear, professional language. Avoid hype but be persuasive.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        return response.choices[0].message.content.strip()

    def _build_blog_prompt(self, factsheet: Dict[str, Any]) -> str:
        """Build the blog post generation prompt."""
        features_str = "\n".join(
            [f"- {feature}" for feature in factsheet.get("key_features", [])]
        )
        specs_str = json.dumps(factsheet.get("technical_specs", {}), indent=2)

        return f"""
Write a professional, engaging 500-word blog post about {factsheet.get('product_name')}.

CRITICAL: The value proposition is the core message - it MUST be prominently featured and reinforced throughout.

Product Information:
- Product Name: {factsheet.get('product_name')}
- Value Proposition: {factsheet.get('value_proposition')}
- Target Audience: {factsheet.get('target_audience')}

Key Features:
{features_str}

Technical Specifications:
{specs_str}

Requirements:
1. Start with a compelling introduction that hooks the reader with the value proposition
2. Explain the key features and how they solve customer problems
3. Highlight the target audience and why this product is perfect for them
4. Use concrete examples or use cases
5. Emphasize the value proposition in the conclusion
6. Maintain a professional, authoritative tone
7. Aim for approximately 500 words
8. Use clear headings and paragraphs for readability
9. End with a call-to-action

Write ONLY the blog post content. No metadata, no "Blog Post:" prefix, just the content.
"""

    def _generate_tweet_thread(self, factsheet: Dict[str, Any]) -> list:
        """
        Generate a 5-tweet thread with engaging tone.

        Args:
            factsheet: Product factsheet dictionary

        Returns:
            List of 5 tweet strings
        """
        prompt = self._build_tweet_prompt(factsheet)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a social media expert. Write engaging, viral-worthy tweets that capture attention and drive engagement. Use emoji strategically, ask questions, and create a compelling narrative. Each tweet should be under 280 characters.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=800,
        )

        content = response.choices[0].message.content.strip()
        tweets = self._parse_tweets(content)

        # Ensure exactly 5 tweets
        if len(tweets) < 5:
            raise ValueError(
                f"Failed to generate 5 tweets. Got {len(tweets)}. Content: {content}"
            )

        return tweets[:5]

    def _build_tweet_prompt(self, factsheet: Dict[str, Any]) -> str:
        """Build the tweet thread generation prompt."""
        features_str = ", ".join(factsheet.get("key_features", [])[:5])

        return f"""
Create a 5-tweet thread about {factsheet.get('product_name')} that is engaging, informative, and viral-worthy.

The thread MUST highlight this value proposition: "{factsheet.get('value_proposition')}"

Product Information:
- Product Name: {factsheet.get('product_name')}
- Value Proposition: {factsheet.get('value_proposition')}
- Target Audience: {factsheet.get('target_audience')}
- Key Features: {features_str}

Requirements for the tweet thread:
1. Tweet 1: Hook the audience with a problem statement or surprising fact. Introduce the product.
2. Tweet 2: Explain the core value proposition. This is key - make it compelling.
3. Tweet 3: Highlight specific features and benefits
4. Tweet 4: Address the target audience directly - why they need this
5. Tweet 5: Call-to-action with a sense of urgency or excitement

Guidelines:
- Each tweet must be under 280 characters
- Use relevant emojis to increase engagement
- Use threads to build narrative momentum
- Include numbers/stats where possible
- Make the value proposition crystal clear
- Write in conversational, engaging tone
- Use "1/" "2/" "3/" "4/" "5/" to number the tweets

Format your response as exactly 5 tweets, one per line, clearly numbered. Example:
1/ Tweet content here...
2/ Tweet content here...
etc.

Do NOT include any explanations or metadata. Just the 5 numbered tweets.
"""

    def _parse_tweets(self, content: str) -> list:
        """
        Parse tweet thread from response.

        Args:
            content: Raw response content

        Returns:
            List of tweet strings
        """
        lines = content.strip().split("\n")
        tweets = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Remove numbering (e.g., "1/", "1.", "1)")
            if line[0].isdigit():
                # Find where the actual tweet starts
                for i, char in enumerate(line):
                    if char in "/.)" and i < len(line) - 1:
                        tweet = line[i + 1 :].strip()
                        if tweet:
                            tweets.append(tweet)
                        break
            elif line:
                tweets.append(line)

        return tweets

    def _generate_email_teaser(self, factsheet: Dict[str, Any]) -> str:
        """
        Generate a compelling email teaser paragraph.

        Args:
            factsheet: Product factsheet dictionary

        Returns:
            Email teaser paragraph
        """
        prompt = self._build_email_prompt(factsheet)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert email copywriter. Write compelling, concise email teasers that drive opens and clicks. Focus on curiosity, benefits, and value. Keep it to one engaging paragraph.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

    def _build_email_prompt(self, factsheet: Dict[str, Any]) -> str:
        """Build the email teaser generation prompt."""
        return f"""
Write a compelling email teaser paragraph for {factsheet.get('product_name')}.

This will be used as the preview/teaser text in an email subject line follow-up or email body opener.

Product Information:
- Product Name: {factsheet.get('product_name')}
- Value Proposition: {factsheet.get('value_proposition')}
- Target Audience: {factsheet.get('target_audience')}

Requirements:
1. Approximately 2-4 sentences (one paragraph only)
2. MUST emphasize the value proposition
3. Create curiosity or urgency
4. Speak directly to the target audience
5. Include a benefit-driven statement
6. Conversational but professional tone
7. Include implied call-to-action (e.g., "Discover how...", "See what's possible...")

Write ONLY the email teaser paragraph. No metadata, no explanations. Just the paragraph text.
"""

    def to_json(self, result: Dict[str, Any]) -> str:
        """
        Convert result to formatted JSON string.

        Args:
            result: The generation result dictionary

        Returns:
            Formatted JSON string
        """
        return json.dumps(result, indent=2)

    def generate_batch(self, factsheets: list) -> list:
        """
        Generate content for multiple factsheets.

        Args:
            factsheets: List of factsheet dictionaries

        Returns:
            List of generation results
        """
        results = []
        for i, factsheet in enumerate(factsheets):
            try:
                result = self.generate_content(factsheet)
                results.append(result)
            except Exception as e:
                results.append(
                    {
                        "status": "error",
                        "timestamp": datetime.utcnow().isoformat(),
                        "error": str(e),
                        "index": i,
                    }
                )
        return results


def main():
    """Example usage of CopywriterAgent."""
    sample_factsheet = {
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
    }

    try:
        agent = CopywriterAgent()
        result = agent.generate_content(sample_factsheet)
        print(agent.to_json(result))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
