# Assignment: Agentic AI — DeepLearning.AI Course

**Course:** [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) by Andrew Ng  
**Platform:** DeepLearning.AI  
**Level:** Intermediate | Self-paced | 5 Modules

---

## 1. Course Summary

**Agentic AI** is an intermediate-level, self-paced course across 5 modules that teaches how to build AI systems capable of autonomous, multi-step workflows — going beyond single-prompt interactions.

### Module Breakdown

| Module | Topic | Focus |
|--------|-------|-------|
| 1 | Introduction to Agentic AI | What makes AI "agentic", identifying suitable tasks, evaluation-driven development |
| 2 | Reflection Design Pattern | AI critiques and improves its own outputs — database querying, chart generation, document writing |
| 3 | Tool Use Design Pattern | Function calling, code execution, Model Context Protocol (MCP) for tool integration |
| 4 | Practical Tips for Building Agentic AI | Evaluations, error analysis, optimization, production deployment |
| 5 | Planning and Multi-Agent Systems | Complex planning, multi-agent coordination for large problems |
| Capstone | Research Agent | Complete autonomous research agent — gather, analyze, report |

### Four Core Design Patterns

- **Reflection** — AI critiques and iteratively improves its own outputs
- **Tool Use** — Connecting AI to databases, APIs, web search, and code execution (including MCP)
- **Planning** — Breaking complex tasks into executable steps with adaptive replanning
- **Multi-Agent Systems** — Coordinating multiple specialized AI agents for complex workflows

---

## 2. What I Learned (Most Important)

1. **Single prompts are not enough for real tasks** — Before this course, I mostly used ChatGPT/Copilot with one-shot prompts. The biggest eye-opener was that breaking a task into multiple agent steps with feedback loops produces dramatically better results.

2. **Reflection is the simplest and most powerful pattern** — Just having an LLM review its own output and try again catches most quality issues. I immediately saw how this applies to code review, writing, and test generation in my daily work.

3. **LLMs can interact with real systems, not just generate text** — Function calling and MCP let agents read databases, call APIs, parse files, and execute code. This changes what's possible — AI can now do actual work, not just suggest it.

4. **Giving agents specialized roles works better than one big prompt** — When I built the POC, splitting the work across 5 focused agents (analyzer, researcher, estimator, reviewer, writer) produced far better proposals than asking one agent to do everything.

5. **You need to test agentic systems differently** — LLM outputs are non-deterministic. The course taught me to build evaluation frameworks and do systematic error analysis — something I hadn't considered before for AI-powered features.

---

## 3. How This Knowledge Can Be Used in My Work at BJIT

As a software engineer at BJIT Limited, I work on client projects that involve requirement analysis, development, code reviews, and documentation. Here are the specific areas where I can apply what I learned:

| My Daily Activity | Agentic Pattern | How I Can Use It |
|---|---|---|
| **Writing code** | Reflection | Use AI to review my code, suggest improvements, and iterate — like having a tireless code reviewer available 24/7 |
| **Project estimation** | Multi-Agent + Planning | Automate requirement breakdown and effort estimation before submitting to leads — reduces back-and-forth |
| **Researching tech solutions** | Tool Use | Let agents search docs, compare libraries, and summarize findings — saves hours of manual research per sprint |
| **Writing docs & READMEs** | Multi-Agent + Reflection | Generate documentation from code, then have a second agent review for clarity and completeness |
| **Writing unit tests** | Tool Use + Reflection | Generate test cases from code, run them, analyze failures, and fix — speeds up test coverage significantly |
| **Client emails & status reports** | Reflection | Draft professional client communications with a quality-check loop — especially useful for non-native English |

The most immediate win for me personally is applying the **reflection pattern** to code review and documentation — these are tasks I do every day, and even a simple "generate then review" loop with an LLM noticeably improves output quality.

---

## 4. POC Proposal

> **ProposalBot** — A multi-agent system that takes requirement documents and produces professional project proposals.

See the full technical proposal: [docs/poc-proposal.md](poc-proposal.md)

This POC directly demonstrates **all four agentic design patterns** from the course:
- **Reflection** → Reviewer agent critiques the estimation and triggers revision
- **Tool Use** → PDF parsing via pdfplumber
- **Planning** → Sequential pipeline orchestration with stage tracking
- **Multi-Agent** → 5 specialized agents coordinated via CrewAI

Supporting documentation:
- [Architecture & Tech Stack](architecture.md)
- [API Design](api-design.md)
- [Agent Pipeline & Reflection Logic](agent-pipeline.md)

---

## 5. My Recommendations & Suggestions

*Based on my personal experience taking this course and building the POC as a software engineer at BJIT Limited:*

1. **This course is practical, not theoretical — more engineers should take it** — Unlike many AI courses that focus on math and theory, this one is hands-on and directly applicable to our daily programming work. I'd recommend BJIT assign this to more engineering teams, especially those working on automation or AI-integrated products.

2. **Start using the reflection pattern immediately — it costs nothing** — Even without building agents, any engineer can improve their output today by adding a simple "review and improve" step when using ChatGPT or Copilot. I've already started doing this for code reviews and documentation, and the quality difference is noticeable.

3. **We should integrate agentic AI into our existing development workflow** — Rather than building new AI products, the fastest ROI is applying these patterns to what we already do: automated code review, test generation, requirement analysis, and documentation. These are daily pain points at BJIT that agentic AI can directly address.

4. **Don't overthink it — start small and iterate** — I initially planned a complex POC with databases, web search, and cloud deployment. But the course taught me to start simple, validate it works, then add complexity. My POC works end-to-end with just 5 agents and in-memory storage. I'd suggest the same approach for any BJIT team trying to adopt agentic AI.

5. **AI doesn't replace engineers — it makes us faster** — After building ProposalBot, my observation is that AI agents are best when they handle the repetitive, time-consuming parts of our work (research, drafting, reviewing) while we focus on design decisions and client understanding. The human-in-the-loop model is the right approach for client deliverables.

6. **Internal knowledge-sharing would multiply the impact** — The four agentic patterns (Reflection, Tool Use, Planning, Multi-Agent) are simple to explain and broadly useful. A 1-hour brown-bag session at BJIT could help other engineers start applying these patterns in their projects immediately.
