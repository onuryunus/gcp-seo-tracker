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

from . import prompt
from .sub_agents.seo_content_evaluator_agent import seo_content_evaluator_agent
from app.sub_agents.edit_content_agent import edit_content_agent

from app.tools.memory import memorize

MODEL = "gemini-2.5-pro"

seo_tracker = LlmAgent(
    name="seo_tracker",
    model=MODEL,
    description=(
        "SEO Tracker analyzes web pages to extract the most commonly used keywords "
        "and checks their compliance with SEO rules. It can also recreate content "
        "in a way that is suitable for SEO optimization. "
        "When a user shares a URL, the request is redirected to the "
        "seo_content_evaluator_agent for keyword and compliance analysis. "
        "If the user wants to make edits or adjustments based on the evaluation, "
        "the request is redirected to the edit_content_agent."
    ),
    instruction=prompt.ROOT_AGENT_PROMPT,
    sub_agents=[
        seo_content_evaluator_agent,
        edit_content_agent
    ],
    tools=[memorize]
)

root_agent = seo_tracker