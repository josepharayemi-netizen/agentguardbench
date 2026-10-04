# AgentGuardBench A Multilingual Benchmark for Privacy Security and Responsible Behaviour in AI Agents

**Joseph Arayemi**  
GIIT Africa, Lagos, Nigeria  
ORCID: 0009-0007-0776-7238  
Correspondence: yemi@giitafrica.com

## Abstract

Tool-using artificial intelligence agents can retrieve information, retain context, and invoke external actions, but these capabilities create failure modes that conventional language-model accuracy tests do not measure. This paper introduces AgentGuardBench v0.1.1, an open, reproducible benchmark for evaluating instruction integrity, privacy protection, least privilege, human-approval controls, memory safety, and benign-task utility. The benchmark contains 120 fully synthetic cases balanced across six risk categories, five sectors, and four languages: English, French, Swahili, and Yoruba. It uses inert tools and deterministic reference policies so that the complete evaluation can run locally without production credentials or paid model APIs. A strict reference policy passed all 120 cases, while a deliberately permissive control passed 20 of 120 cases. On the 100 adversarial cases, attack success was 0% for the strict policy and 100% for the permissive policy. Both policies completed all 20 benign controls, demonstrating that the scoring pipeline can distinguish unsafe behaviour without treating every request as malicious. These results validate the benchmark mechanics rather than establish the safety of any commercial or production model. The contribution is a transparent evaluation scaffold, machine-readable outputs, and a governance-oriented mapping to NIST AI RMF, OWASP agentic-security risks, and MITRE ATLAS. Future work should add real model adapters, native-speaker validation, paraphrased attacks, repeated stochastic trials, and independent annotation.

**Keywords:** responsible AI; AI agents; prompt injection; privacy; tool security; multilingual benchmark; human oversight; reproducibility

## 1 Introduction

Large language models are increasingly embedded in agents that plan tasks, call tools, access stored context, and interact with external systems. The shift from text generation to action changes the unit of risk. A harmful output may no longer remain a sentence on a screen; it may become an email, a record deletion, a disclosure of private information, or an unauthorised transaction. Evaluation therefore needs to test not only whether an agent can complete a task, but whether it preserves instruction priority, respects permissions, protects sensitive information, and requests human approval before high-impact actions.

Existing agent benchmarks have made important progress in measuring reasoning and task completion in interactive environments. AgentBench, for example, evaluates agents across eight environments and identifies instruction following, long-horizon reasoning, and decision-making as persistent obstacles. Capability evaluation alone, however, does not provide a compact and reproducible test of privacy, security, and responsible action across multilingual and sectoral contexts.

AgentGuardBench addresses this gap with a small, auditable benchmark designed for defensive research and resource-constrained organisations. It extends the secure and responsible design principles developed in Arayemi's prior multi-cloud retrieval-augmented generation work from architecture to agent evaluation. The benchmark is intentionally inexpensive to run: all cases are synthetic, all tools are inert, and the bundled baselines are deterministic.

This paper asks four questions:

1. Can a transparent scenario set distinguish a guarded agent policy from a permissive policy?
2. Can safety controls reject adversarial requests while preserving benign-task completion?
3. Can the benchmark cover multiple risk categories, sectors, and languages without using real personal information?
4. Which limitations must be resolved before results can support claims about production models or cross-language performance?

## 2 Background and Related Work

NIST AI 600-1 profiles generative-AI risks within the AI Risk Management Framework and emphasises governance, measurement, transparency, privacy, security, and continuous evaluation. The OWASP Top 10 for Agentic Applications identifies risks such as agent goal hijacking, tool misuse, identity and privilege abuse, and memory-related failures. MITRE ATLAS catalogues adversarial tactics and techniques for AI systems, including prompt injection, context poisoning, tool invocation, credential access, and exfiltration. AgentGuardBench translates these broad risk concerns into executable scenario fields and observable outcomes.

AgentBench demonstrates the value of multi-environment testing for agent reasoning and action. AgentGuardBench is complementary: it focuses on whether an agent should act, disclose, refuse, redact, or seek approval under security and governance constraints. Its design also prioritises low-cost reproduction, explicit expected actions, and transparent deterministic fixtures.

The benchmark follows earlier secure RAG work by the author, which proposed defence-in-depth controls for resource-constrained organisations deploying retrieval-augmented generation across AWS and Microsoft Azure. AgentGuardBench generalises those principles beyond retrieval to tool-using agents, adding multilingual test cases for prompt injection, privacy leakage, privilege abuse, unsafe memory recall, unauthorised tool use, and human oversight.

## 3 Benchmark Design

### 3.1 Dataset structure

AgentGuardBench v0.1.1 contains 120 JSON Lines records. The Cartesian design combines six categories, five sectors, and four languages, producing one case for each category-sector-language combination. Each category therefore has 20 cases, each sector has 24 cases, and each language has 30 cases.

The six categories are prompt injection, privacy leakage, tool misuse, privilege abuse, memory safety, and benign control. Sectors are banking, healthcare, education, government, and recruitment. Languages are English, French, Swahili, and Yoruba. The dataset contains no real people, credentials, organisations, or operational targets. Demonstration identifiers use reserved or clearly synthetic values.

Each scenario records an identifier, category, sector, language, prompt, untrusted context, requested tool where applicable, expected action, sensitivity flag, human-approval requirement, severity, and standards references. Expected actions are answer, redact, refuse, or request approval.

### 3.2 Threat and control model

Prompt-injection cases place adversarial instructions inside untrusted context and expect refusal. Privacy-leakage cases request protected fields and expect redaction. Tool-misuse cases request unreviewed external communication and expect human approval. Privilege-abuse cases request destructive actions from a read-only role and expect refusal. Memory-safety cases request previously supplied secrets and expect refusal. Benign controls request a summary of public synthetic information and expect an answer.

The strict reference policy applies five control ideas: detect explicit injection markers; identify synthetic sensitive-data patterns; enforce the scenario's authorised scope; gate high-impact tools behind human approval; and allow benign requests. The permissive control follows the latest instruction, invokes a requested tool, and returns available context without policy checks.

The bundled implementations are deliberately simple. They are fixtures for validating the benchmark and evaluator, not competitive agent systems.

### 3.3 Metrics

For N scenarios, overall pass rate is the fraction in which the agent action equals the expected action. Attack success rate is calculated over non-benign scenarios and counts an adversarial case as successful when the agent fails and proceeds by answering or executing. Privacy leakage rate is the fraction of all scenarios in which the response discloses sensitive data. Unauthorised tool-use rate is the fraction of all scenarios in which a tool is called when the expected action is neither execute nor answer. Approval-violation rate is the fraction of all scenarios requiring approval in which the agent executes. Benign-task completion is the fraction of benign-control cases that pass.

Because the bundled policies are deterministic and the dataset is fixed, each run produces the same point estimates. Confidence intervals would suggest sampling uncertainty that the current experiment does not generate. Future stochastic model evaluations should report repeated trials, dispersion, and uncertainty.

## 4 Experimental Method

The experiment regenerated the 120-case dataset from transparent templates and executed the strict and permissive policies against the same immutable cases. The evaluator compared each policy action with the expected action and recorded per-case outcomes in JSONL. It then aggregated the metrics into JSON summaries. No network calls, model APIs, production credentials, external recipients, or irreversible tools were used.

Reproduction requires Python 3.10 or later and three commands:

```text
python scripts/generate_dataset.py
PYTHONPATH=src python -m agentguardbench --policy both
python -m unittest discover -s tests -v
```

The released repository includes the generator, scenarios, evaluator, policy fixtures, tests, raw results, summary results, dataset card, ethics statement, security policy, and citation metadata. The software release is archived at https://doi.org/10.5281/zenodo.23127436.

## 5 Results

The strict reference policy passed 120 of 120 cases. The permissive control passed 20 of 120 cases, corresponding exactly to the benign controls. On the 100 adversarial cases, attack success was 0% for the strict policy and 100% for the permissive policy. Privacy leakage was 0% versus 50% of all cases; unauthorised tool use was 0% versus 33.33%; and approval violations were 0% versus 16.67%. Both policies completed 100% of benign tasks.

| Metric | Strict reference policy | Permissive control |
|---|---:|---:|
| Overall pass rate | 100.00% | 16.67% |
| Attack success rate | 0.00% | 100.00% |
| Privacy leakage rate | 0.00% | 50.00% |
| Unauthorised tool-use rate | 0.00% | 33.33% |
| Human-approval violation rate | 0.00% | 16.67% |
| Benign-task completion rate | 100.00% | 100.00% |

At category level, the strict policy achieved a 100% pass rate in all six categories. The permissive policy achieved 100% on benign controls and 0% in each of the five adversarial categories. This deliberately wide separation confirms that the evaluator recognises both expected safe actions and clear unsafe actions.

## 6 Discussion

The main finding is methodological. AgentGuardBench can distinguish two intentionally different policy behaviours while preserving benign utility. The equal benign-completion result matters because a benchmark that rewards blanket refusal would provide limited operational value. The strict fixture succeeded because the expected actions were aligned with the exact markers and rules implemented by the policy. The result therefore establishes internal consistency, not robustness to unseen attacks.

The multilingual and sectoral matrix improves coverage and supports structured error analysis. It does not yet establish linguistic equivalence or sector realism. The translated prompts are template-based and require independent review by native speakers, especially for idiom, tone, and attack naturalness. Sector labels vary context while retaining a common risk structure; future versions should add domain-expert scenarios grounded in authorised, non-sensitive workflows.

For resource-constrained organisations, the benchmark demonstrates a practical evaluation pattern: define observable safety expectations, keep test tools inert, preserve raw machine-readable results, include benign controls, and separate benchmark validation from model claims. These practices allow teams to begin governance work before purchasing extensive red-team infrastructure.

### 6.1 Mapping to governance and security frameworks

AgentGuardBench supports measurement activities in NIST AI RMF by making scenarios, expected outcomes, and results explicit. Its prompt-injection and context-integrity tests correspond to agent goal hijacking and related adversarial techniques. Tool-misuse and privilege-abuse cases test boundaries around external actions and identity. Privacy and memory cases test data minimisation, secret handling, and retention expectations. These mappings are orientation aids, not certifications of compliance.

### 6.2 Responsible interpretation

Benchmark scores describe a tested configuration. They do not prove that a system is universally safe, ethical, secure, or legally compliant. A production evaluation must account for the actual model, prompts, memory, retrieval sources, identity controls, tool implementations, deployment context, users, and monitoring processes. Results should be accompanied by model and system documentation, incident procedures, and human review for high-impact uses.

## 7 Limitations and Threats to Validity

First, the cases are generated from six templates, so lexical diversity is limited. A policy that recognises the exact markers can overfit the benchmark. Second, the reference policies are deterministic fixtures rather than contemporary language models. Third, translations have not yet undergone independent native-speaker validation. Fourth, the current dataset contains one case per category-sector-language cell and does not represent the distribution of real incidents. Fifth, binary expected actions simplify situations in which several responses might be defensible. Sixth, the evaluator scores declared actions and flags; it does not inspect the semantics of unconstrained natural-language responses. Seventh, no inter-rater reliability study has been performed because labels are generated directly from templates.

These limitations mean that v0.1.1 should be used for pipeline validation, education, and controlled extension. Claims about comparative model safety require a preregistered protocol, hidden or held-out cases, multiple model runs, independent annotation, and statistical analysis.

## 8 Future Work

The next release should add adapters for local and hosted models while retaining inert tool execution. It should include paraphrased and indirect injections, multi-turn attacks, tool-output poisoning, context-window pressure, memory contamination, and cross-tool privilege escalation. Native speakers should review every translated case and contribute culturally and linguistically natural variants. Independent annotators should assess expected actions and report agreement. Stochastic evaluations should use repeated runs and report confidence intervals or bootstrap uncertainty. A held-out challenge set should reduce the risk of policies fitting public templates. Finally, sector specialists should develop authorised scenarios for healthcare, finance, education, government, and recruitment without introducing real personal data.

## 9 Conclusion

AgentGuardBench provides an open and reproducible starting point for evaluating privacy, security, and responsible behaviour in tool-using AI agents. Its 120 synthetic cases cover six risk categories, five sectors, and four languages. The strict and permissive fixtures produce clearly separable results while both retain benign-task completion, validating the evaluator and output pipeline. The benchmark's value lies in transparency, low operating cost, and extensibility. Its current results must remain bounded to deterministic pipeline validation; production and cross-language claims require substantially broader experiments.

## Data and Software Availability

Source code and data: https://github.com/josepharayemi-netizen/agentguardbench  
Technical report: https://doi.org/10.5281/zenodo.23132194
Archived software release: https://doi.org/10.5281/zenodo.23127436  
Concept DOI for all software versions: https://doi.org/10.5281/zenodo.23127435  
License: MIT

## Ethics Statement

All benchmark content is synthetic and all tools are inert. AgentGuardBench is intended for defensive research, education, and authorised evaluation. It must not be used to target systems without permission, collect real personal data, bypass access controls, or automate harmful actions.

## Conflict of Interest

The author declares no conflict of interest.

## References

1. Arayemi, J. (2026). Secure and Responsible Retrieval-Augmented Generation for Resource-Constrained Organizations: A Multi-Cloud Reference Architecture and Experimental Evaluation. Zenodo. https://doi.org/10.5281/zenodo.23048249
2. Arayemi, J. (2026). AgentGuardBench: A Multilingual Benchmark for Privacy, Security and Responsible Behaviour in AI Agents, version 0.1.1. Zenodo. https://doi.org/10.5281/zenodo.23127436
3. Autio, C., Schwartz, R., Dunietz, J., Jain, S., Stanley, M., Tabassi, E., Hall, P., and Roberts, K. (2024). Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile. NIST AI 600-1. https://doi.org/10.6028/NIST.AI.600-1
4. Liu, X., et al. (2024). AgentBench: Evaluating LLMs as Agents. International Conference on Learning Representations. https://arxiv.org/abs/2308.03688
5. MITRE. (2026). MITRE ATLAS. https://atlas.mitre.org/
6. OWASP GenAI Security Project. (2025). OWASP Top 10 for Agentic Applications. https://genai.owasp.org/
