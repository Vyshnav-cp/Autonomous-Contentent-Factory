import json
from typing import Optional
from datetime import datetime
from openai import OpenAI
import os


class ResearchAgent:
    """
    An AI agent that analyzes raw text input to extract structured product information.
    Uses OpenAI's API to intelligently parse and categorize product details.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the ResearchAgent with OpenAI client.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
            model: The OpenAI model to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def analyze(self, raw_text: str) -> dict:
        """
        Analyze raw text input and extract structured product information.

        Args:
            raw_text: The input text describing a product

        Returns:
            A dictionary containing extracted information with the following keys:
            - product_name: Name of the product
            - key_features: List of main features
            - technical_specs: Technical specifications
            - target_audience: Intended audience for the product
            - value_proposition: Core value offered
            - ambiguous_statements: List of unclear or vague claims
            - timestamp: When analysis was performed
            - raw_input_length: Character count of input
        """
        if not raw_text or not raw_text.strip():
            raise ValueError("Input text cannot be empty")

        prompt = self._build_extraction_prompt(raw_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert product analyst. Extract and structure product information from raw text. Always respond with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            extracted_data = json.loads(response.choices[0].message.content)
            result = self._format_result(extracted_data, raw_text)

            return result

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse API response as JSON: {e}")
        except Exception as e:
            raise Exception(f"Error during API call: {e}")

    def _build_extraction_prompt(self, raw_text: str) -> str:
        """
        Build the prompt for OpenAI to extract product information.

        Args:
            raw_text: The raw product description text

        Returns:
            A formatted prompt string
        """
        return f"""
Analyze the following product description and extract structured information.
Return a valid JSON object with these exact keys:

1. "product_name": The name or title of the product (string). If not explicitly mentioned, infer from context or return "Unknown".
2. "key_features": A list of the main features and capabilities (array of strings). Extract the most important characteristics.
3. "technical_specs": An object containing technical specifications and details (object). Include any measurements, dimensions, performance metrics, etc.
4. "target_audience": Description of who this product is intended for (string). Include demographics, use cases, or customer segments.
5. "value_proposition": The core value or main benefit offered to customers (string). What problem does it solve or what need does it fulfill?
6. "ambiguous_statements": A list of unclear, vague, or unsubstantiated claims found in the text (array of strings). Flag any marketing hype, undefined terms, or unsupported assertions.

Product Description:
---
{raw_text}
---

Return ONLY valid JSON with the structure above. Ensure all strings are properly escaped. Leave any empty or unavailable fields as empty strings or empty arrays/objects.
"""

    def _format_result(self, extracted_data: dict, raw_text: str) -> dict:
        """
        Format the extracted data with metadata and validation.

        Args:
            extracted_data: The data extracted from OpenAI
            raw_text: The original input text

        Returns:
            A formatted result dictionary
        """
        result = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "raw_input_length": len(raw_text),
            "analysis": {
                "product_name": extracted_data.get("product_name", "Unknown"),
                "key_features": extracted_data.get("key_features", []),
                "technical_specs": extracted_data.get("technical_specs", {}),
                "target_audience": extracted_data.get("target_audience", ""),
                "value_proposition": extracted_data.get("value_proposition", ""),
                "ambiguous_statements": extracted_data.get("ambiguous_statements", []),
            },
        }
        return result

    def analyze_batch(self, texts: list) -> list:
        """
        Analyze multiple product descriptions in sequence.

        Args:
            texts: List of raw text inputs

        Returns:
            List of analysis results
        """
        results = []
        for i, text in enumerate(texts):
            try:
                result = self.analyze(text)
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

    def to_json(self, result: dict) -> str:
        """
        Convert analysis result to formatted JSON string.

        Args:
            result: The analysis result dictionary

        Returns:
            Formatted JSON string
        """
        return json.dumps(result, indent=2)


def main():
    """Example usage of ResearchAgent."""
    # Example product description
    sample_text = """
    The CloudVault Pro is a revolutionary cloud storage solution designed for enterprises.
    It offers unlimited storage capacity with military-grade encryption. The platform supports
    real-time collaboration for teams up to 1000 members. It seamlessly integrates with
    popular productivity tools and provides AI-powered automatic file organization.
    With our advanced analytics, you'll get unprecedented insights into your data.
    Perfect for businesses looking to transform their digital infrastructure.
    Available in Standard, Professional, and Enterprise tiers.
    """

    try:
        # Initialize the agent
        agent = ResearchAgent()

        # Analyze the product description
        result = agent.analyze(sample_text)

        # Print results as formatted JSON
        print(agent.to_json(result))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
