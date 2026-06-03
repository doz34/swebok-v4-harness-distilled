# SWEBOK v4 Harness V2 — Distilled Knowledge Engine
# Multi-stage build: minimal runtime, no LLM deps by default.
#
# Build:   docker build -t swebok-v4-harness-distilled:2.0 .
# Run L0:  docker run --rm swebok-v4-harness-distilled:2.0 "What is SOLID?"
# Run L1:  docker run --rm -v /path/to/corpus:/corpus swebok-v4-harness-distilled:2.0 \
#            bash -c "python3 scripts/retrieval/pipeline.py /corpus/ --output /tmp/idx.json && \
#                     python3 scripts/query.py --dossier 'your question'"

FROM python:3.11-slim

LABEL maintainer="swebok-v4-harness" \
      version="2.0.0" \
      description="Compiled + multi-view retrieval over a corpus. Deterministic by default."

# Use a non-root user for runtime
RUN groupadd -r harness && useradd -r -g harness harness
WORKDIR /app

# Copy harness code
COPY --chown=harness:harness scripts/ /app/scripts/
COPY --chown=harness:harness distilled/ /app/distilled/
COPY --chown=harness:harness docs/ /app/docs/
COPY --chown=harness:harness README.md /app/
COPY --chown=harness:harness CLAUDE.md /app/
COPY --chown=harness:harness LICENSE /app/

# Default to deterministic (no LLM required). Override at runtime:
#   docker run -e SWEBOK_PROVIDER=openai -e OPENAI_API_KEY=... ...
ENV SWEBOK_PROVIDER=deterministic \
    PYTHONUNBUFFERED=1

USER harness

# Healthcheck: invoke the --health probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 scripts/query.py --health || exit 1

# Default entrypoint: L0 query
ENTRYPOINT ["python3", "scripts/query.py"]
CMD ["--help"]
