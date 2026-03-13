from typing import Literal
from google.adk.agents import Agent
from google.adk.apps.app import App
from pydantic import BaseModel, Field


MODEL = "gemini-2.5-pro"

# 1. Define the Schema
# It extends BaseModel and defines 'status' ("pass" or "fail") and 'feedback'.
class JudgeFeedback(BaseModel):
    """Structured feedback from the Judge agent."""
    status: Literal["pass", "fail"] = Field(
        description="Whether the research is sufficient ('pass') or needs more work ('fail')."
    )
    feedback: str = Field(
        description="Detailed feedback on what is missing. If 'pass', a brief confirmation."
    )

# 2. Define the Agent
# The judge should accept research findings, evaluate them, and output the JudgeFeedback schema.
judge = Agent(
    name="judge",
    model=MODEL,
    description="Evaluates research findings for completeness and accuracy.",
    instruction="""
    You are a strict editor.
    Evaluate the 'research_findings' against the user's original request.
    If the findings are missing key info, return status='fail'.
    If they are comprehensive, return status='pass'.
    """,
    output_schema=JudgeFeedback,
    # Disallow delegation because it should only output the schema
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

root_agent = judge