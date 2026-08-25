"""AdversarialDebate: two isolated LLM reviewers, bounded debate, preserved dissent.

Implements PRD [02-architecture](docs/design/prd/02-architecture.md). The one
non-negotiable invariant: reviewer B cannot see reviewer A's output until B has
fully committed its own review — and vice versa (PRD §2.3).
"""

__version__ = "0.1.0"
