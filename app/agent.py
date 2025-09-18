# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""SEO Tracker Agent analyzes web pages for SEO optimization and content improvement."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.content_seo_ruler import content_seo_ruler_agent
from .sub_agents.seo_content_recreator import seo_content_recreator_agent
from .sub_agents.html_content_extractor import html_content_extractor_agent
from .sub_agents.image_generator import image_generator_agent

MODEL = "gemini-2.5-pro"

seo_tracker = LlmAgent(
    name="seo_tracker",
    model=MODEL,
    description=(
        "SEO Tracker analyzes web pages to extract the most commonly used keywords "
        "and checks their compliance with SEO rules. It can also recreate content "
        "in a way that is suitable for SEO optimization, generate high-quality images "
        "with SEO-optimized alt texts, and improve accessibility by creating alt text "
        "suggestions for existing web page images."
    ),
    instruction=prompt.SEO_TRACKER_PROMPT,
    tools=[
        # AgentTool(agent=content_seo_ruler_agent),
        # AgentTool(agent=seo_content_recreator_agent),
        AgentTool(agent=html_content_extractor_agent),
        AgentTool(agent=image_generator_agent),
    ],
)

root_agent = seo_tracker