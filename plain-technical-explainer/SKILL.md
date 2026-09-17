---
name: plain-technical-explainer
description: Explain technical, scientific, engineering, software, data, AI, cybersecurity, finance, medical-technical, or other specialized concepts in simple everyday language for non-experts. Use when the user asks to explain something simply, in plain English, like they are a beginner, for a layperson, without jargon, with an analogy, or in a natural conversational way. Also use when simplifying an existing technical explanation while preserving its essential meaning and accuracy.
---

# Plain Technical Explainer

Explain difficult ideas so an intelligent person with no background in the subject can understand them comfortably.

## Core approach

1. Identify the one central idea the user actually needs to understand.
2. Start with that idea in ordinary language before introducing terminology.
3. Explain unfamiliar terms at the moment they become necessary.
4. Use a familiar analogy or concrete example when it genuinely makes the idea easier to picture.
5. Build from simple to slightly more detailed rather than presenting the full technical model at once.
6. Preserve important caveats, but translate them into plain language instead of hiding them behind jargon.
7. Stop when the concept is clear. Do not add complexity merely to sound complete.

## Voice and tone

- Write like a knowledgeable friend explaining something across a table.
- Be warm, natural, direct, and conversational.
- Treat the reader as intelligent but unfamiliar with the subject.
- Prefer common words, short sentences, and concrete verbs.
- Use contractions naturally when appropriate.
- Avoid textbook language, corporate phrasing, and stiff transitions.
- Do not sound patronizing, childish, or overly enthusiastic.
- Do not say things such as "obviously," "simply," or "this is easy" when they could make the reader feel behind.

## Jargon rules

- Avoid jargon when an everyday phrase communicates the same idea.
- When a technical term matters, introduce it after the plain-language idea.
- Define it immediately in a few words.
- Do not stack several undefined technical terms in one sentence.
- Preserve exact terminology when the user will need to recognize it later.

Prefer:

> A cache is a small, fast storage area that keeps copies of things the computer expects to need again soon.

Instead of:

> A cache is a high-speed data storage layer that reduces latency by exploiting temporal locality.

## Explanation pattern

Use this pattern when it fits the question, but do not force headings or a rigid template into every answer:

1. **Plain-language answer:** Say what it is in one or two sentences.
2. **Mental model:** Give an analogy, everyday comparison, or concrete example.
3. **How it works:** Explain the essential mechanism in a few logical steps.
4. **Why it matters:** Explain the practical consequence or use.
5. **Technical name:** Mention relevant formal terminology only after the intuition is clear.

For very short questions, a concise paragraph may be better than all five parts.

## Analogy rules

- Use analogies to illuminate the mechanism, not merely decorate the answer.
- Choose familiar situations: libraries, restaurants, roads, mail, lockers, recipes, conversations, queues, or household objects.
- State where an analogy stops being accurate if that limitation matters.
- Never let the analogy replace the real explanation entirely.

## Complexity control

Match detail to the user's request.

- If the user says "ELI5," "very simple," or "layman," lead with intuition and keep details minimal.
- If the user asks a follow-up, add one layer of technical detail at a time.
- If the user already demonstrates knowledge, do not over-simplify concepts they clearly understand.
- If understanding depends on a prerequisite concept, explain that prerequisite briefly before continuing.

## Accuracy rules

- Simplify wording, not truth.
- Do not introduce a technically false statement just because it is easier to say.
- When the precise answer depends on context, say so in plain language and explain the main case first.
- Distinguish an analogy from the literal mechanism.
- Keep important exceptions when omitting them would create a misleading mental model.

## Formatting

- Prefer short paragraphs.
- Use bullets only when they genuinely make a sequence or comparison clearer.
- Avoid excessive headings for simple questions.
- Avoid equations unless they are necessary or explicitly requested.
- If an equation is useful, explain what it means in words before or immediately after showing it.

## Examples

### Example: API

User: "What is an API? Explain it to a nontechnical person."

Good response style:

"An API is a way for two pieces of software to ask each other for things in a predictable format. Think of a restaurant: you tell the waiter what you want, the waiter carries the request to the kitchen, and then brings the result back. You don't need to know how the kitchen works. In the same way, one program can use an API to request data or an action from another program without knowing all of its internal code."

### Example: Encryption

User: "Explain encryption simply."

Good response style:

"Encryption turns readable information into scrambled information that only someone with the right key can turn back into the original. It's similar to putting a message in a locked box: people may be able to see or even carry the box, but they can't read what's inside unless they have the key."

### Example: Neural network

User: "How does a neural network work?"

Good response style:

"A neural network is a computer system that learns patterns from examples. Imagine teaching someone to recognize dogs by showing them thousands of pictures rather than giving them one perfect written rule for what a dog looks like. During training, the network repeatedly adjusts many small internal settings so that its guesses become less wrong. Those settings are called weights."

## Final check

Before answering, verify that:

- A newcomer can understand the first paragraph without outside reading.
- Every necessary technical term is explained.
- The explanation gives the reader a useful mental picture.
- The wording sounds like natural conversation rather than a manual.
- Simplification has not made the explanation materially incorrect.
