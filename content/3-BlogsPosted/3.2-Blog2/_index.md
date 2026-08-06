---
title: "Combining AWS CLI & Hermes Agent"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 3.2. </b> "
---

# Combining AWS CLI & Hermes Agent: Bringing AI into Cloud Management with Natural Language

> \*Original post on Facebook: [AWS Study Group - Blog 2](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2236254263806200/?rdid=98lGo4WwJK4aSNns#)\*

When configuring AWS infrastructure via the Web Console becomes tedious, and memorizing hundreds of complex AWS CLI commands starts to challenge developers, an interesting question arises: *Can we communicate with the cloud in our own natural language?*

Below is an outline of a proposal to combine **AWS CLI** and **Hermes Agent** - turning AI into a "DevOps Assistant" that controls infrastructure using natural language. This article is shared as a discussion proposal, and I look forward to receiving feedback, experience, and perspectives from fellow developers and system engineers!

---
{{< img src="/images/Blog2.png" alt="AWS CLI & Hermes Integration" >}}

## 1. Brief Introduction of Both Technologies

*   **AWS CLI (Amazon Web Services Command Line Interface):** Amazon's open-source command-line tool that helps manage, configure, and automate all AWS resources through Terminal/Command Prompt instead of clicking on the Console.
*   **Hermes Agent:** An open-source AI Agent Framework by [Nous Research](https://github.com/NousResearch/hermes-agent), designed specifically to run directly on the user's terminal, supporting powerful code execution and interaction with system tools (tool use).

---

## 2. Combination Plan (General Idea)

The core idea is to set up an integrated runtime environment where **Hermes Agent** acts as the "brain" receiving natural language, translating requests, and executing **AWS CLI** commands directly via system tools:

1.  **Environment Configuration:** Authenticate AWS credentials on the local host or container environment where Hermes Agent is running.
2.  **Communication Routing:** Connect Hermes Agent to a user-friendly chat interface (e.g., Telegram, Discord, or Slack Chatbot) via Webhook or API.
3.  **Processing Loop:** When the user sends a request in natural language (Vietnamese or English), Hermes Agent will detect the intent, convert it into an AWS CLI command, execute it via the internal command-line tool, then format and return the result to the user.

---

## 3. Expected Outcomes

*   **Hands-free Cloud Administration:** System engineers or developers can check EC2 instance status, check S3 storage capacity, or create IAM accounts using normal chat messages on mobile phones or team collaboration apps.
*   **Easy for Beginners:** New members of the development team do not need to memorize a series of complex AWS CLI parameters but can still perform some basic tasks safely under AI supervision.

---

## 4. Feasibility Assessment

*   **Feasibility: Very High.**
*   **Reason:** Hermes Agent already has a built-in `terminal` tool that supports executing local system commands. AWS CLI also runs independently as a command-line tool and uses static authentication configuration files. Therefore, connecting these two technologies is only a matter of environment setup and command-line permissions, without any complex technical barriers at the core level.

---

## 5. Key Strengths

*   **Natural and Multi-channel Communication:** Excellent support for natural language, allowing commands in natural language. It can easily connect via social network chatbots to manage infrastructure anytime, anywhere.
*   **Self-learning and Evolution (Skills):** Hermes Agent has an autonomous "Skills" creation mechanism. Once a complex workflow is completed, it can save it as a skill for reuse, making it smarter over time in practice.

---

## 6. Current Weaknesses and Bottlenecks

*   **High Token Consumption (Costly):** AI Agents operate on reasoning loops and call multiple sub-tools, consuming a significant amount of tokens for each request.
*   **API Limits & Brain Cost:** To save costs, the current solution uses free models through **OpenRouter**. However, OpenRouter has recently tightened rate limits on free accounts, reducing system stability. We are still looking for optimal alternatives (such as running small local models or finding other low-cost API providers).

---

## Conclusion & Discussion

Combining AI Agents with cloud infrastructure management opens up many opportunities to optimize work efficiency, but also comes with token costs and model stability challenges.

Please share your opinions, experiences, or suggestions in the comments below!