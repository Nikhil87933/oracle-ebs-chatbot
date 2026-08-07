# ADR-0001: Initial Project Architecture

- **Status:** Accepted
- **Date:** 2026-08-07

## Context

A consistent architecture is required for developing the Oracle EBS AI Chatbot Proof of Concept.

## Decision

The project will use:

- Oracle APEX for the user interface
- FastAPI for the backend
- A local LLM for natural language processing
- Oracle EBS as the data source
- The Enterprise Python Template as the project foundation

## Consequences

- Clear separation between UI, backend, AI, and Oracle integration.
- The architecture may evolve as the project progresses.