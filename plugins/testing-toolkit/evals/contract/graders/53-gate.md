---
type: llm
weight: 2
---

Pass if the final message tells the user about the steps that follow the consumer test: the provider has to verify the pact, and deploys are gated with can-i-deploy or the pact broker.

Fail if the message mentions neither provider verification nor can-i-deploy.
