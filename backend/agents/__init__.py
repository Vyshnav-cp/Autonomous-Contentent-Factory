"""
Autonomous Content Factory - Agents Module

This module contains AI agents for various content generation and analysis tasks.
"""

from .research_agent import ResearchAgent
from .copywriter_agent import CopywriterAgent
from .editor_agent import EditorAgent
from .campaign_service import CampaignService

__all__ = ["ResearchAgent", "CopywriterAgent", "EditorAgent", "CampaignService"]

__version__ = "0.4.0"
