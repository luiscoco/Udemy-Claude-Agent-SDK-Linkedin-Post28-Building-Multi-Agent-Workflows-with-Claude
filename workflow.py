"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    plan = await agent.ask('planner', 'Plan exactly three sections for the requested beginner article.', data, {'sections': ['Problem', 'Async iteration', 'Practice']})
    if len(plan['sections']) != 3:
        raise ValueError('The article contract requires three sections')
    findings = await agent.ask('researcher', 'Extract supported findings and source IDs for this plan.', {'plan': plan, 'sources': data['sources']},
                               {'findings': ['async for consumes an asynchronous iterator. [S1]']})
    article = await agent.ask('writer', 'Write the planned article using only the supplied evidence and source IDs.', {'plan': plan, 'research': findings},
                             '# Async Python\n\n## Problem\nWaiting need not block other work.\n\n## Async iteration\nUse async for. [S1]\n\n## Practice\nInspect an async iterator.')
    return {'plan': plan, 'findings': findings, 'article': article}
