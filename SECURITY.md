# Security and privacy notes

## Scope

This describes data and operational risks visible in the static knowledge-base repository. It is not a security, privacy, legal, or compliance certification.

## Content classification

The business profile and conversation material include business/contact details and claims about customers, results, guarantees, prices, competitors, and service operations. Some content may be confidential, personal, commercially sensitive, regulated, stale, or unsupported. The repository does not provide a data inventory, source citations, consent records, retention rules, or owner approvals. Review the content register before publishing or loading files into a third-party model.

## External model use

No runtime is included, but the system prompt instructs users to paste content into an LLM and use JSON files as retrieval context. A provider may receive the prompt and retrieved passages. Verify current provider terms and data handling, minimize submitted content, and do not send personal, client-confidential, credential, financial, or sensitive data without authorization and an approved data-processing basis.

## Visitor data and lead capture

The former prompt encouraged collection of email, phone, budget, and other lead context without defining consent, storage, deletion, or access controls. It has been revised to require data minimization and explicit consent. No implementation of those controls exists in this repository.

## Generated PDFs

PDF files are tracked snapshots that may repeat source claims and contact details. They have not been checked against the revised prompt or reviewed content. Do not distribute them as approved collateral until they are rebuilt from approved material and inspected.

## Evidence limits

No application, provider integration, access-control configuration, logging policy, retention/deletion process, security tests, or privacy review is included in the tracked tree.
