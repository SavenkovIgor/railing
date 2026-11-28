# Docker best practices

Target outcomes: speed, security, reliability.
Speed achieved with minimalist images, caching, and BuildKit features.
Security achieved with least-privilege, secret handling, and small attack surface.
Reliability achieved with deterministic builds, health checks, and proper signal handling.

## Rule 1: Use the smallest viable base image

Problem: Fat base images increase CVE surface and pull time.
Solution: Choose image by runtime needs: `alpine` for static bins, `slim` for glibc apps, `distroless`/`scratch` for prod-only runtime.
Reasoning: Less OS stuff = fewer vulnerabilities and faster shipping.
Avoid: `FROM ubuntu:latest # 200+ MB`
Example: `FROM python:3.11.4-slim`

## Rule 2: Never use `latest` tags

Problem: `latest` is non-deterministic; same Dockerfile can produce different images cuz upstream moves.
Solution: Pin exact tags for base images and toolchains.
Reasoning: Reproducible builds make rollback/debug much easier.
Avoid: `FROM python:latest`
Example: `FROM node:18.20.3-alpine3.20`

## Rule 3: Keep build context clean with `.dockerignore`

Problem: Sending junk (`.git`, `node_modules`, `.env`) slows build and may leak secrets.
Solution: Exclude everything not needed for build.
Reasoning: Smaller context = faster and safer builds.
Example:

```dockerignore
.git
node_modules/
.env
```

## Rule 4: Optimize layer order for cache hits

Problem: If a top layer changes, all following layers rebuild.
Solution: Put rarely changed stuff first (deps), frequently changed code last.
Reasoning: Better cache locality cuts CI time hard cuz cache hits stay high.
Example:

```dockerfile
COPY package*.json ./
RUN npm ci
COPY . .
```

## Rule 5: Merge related `RUN` steps and clean in same layer

Problem: Every `RUN` adds a layer; cleaning in another layer does not shrink previous one.
Solution: Install + cleanup in one `RUN`.
Reasoning: Fewer layers and no stale package cache.
Example:

```dockerfile
# Everything in one RUN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

## Rule 6: Prefer `COPY` over `ADD`

Problem: `ADD` has magic behavior (URL download, auto-unpack), which is less predictable.
Solution: Use `COPY` for files; use explicit `RUN curl|tar` when needed.
Reasoning: Explicit build logic is easier to cache, audit, and debug.
Avoid: `ADD https://prostodevops.ru/file.tar.gz /app/`
Example: `COPY local.txt /app/`

## Rule 7: Use multi-stage builds

Problem: Shipping build toolchain in runtime image bloats size and risk.
Solution: Build in heavy stage, copy only runtime artifact to final stage.
Reasoning: Lean runtime image, smaller attack surface, faster deploy.
Example:

```dockerfile
FROM golang:1.21 AS builder # Stage 1: build
RUN go build -o /app
FROM alpine # Stage 2: clean runtime
COPY --from=builder /app /app # Copy ONLY binary from builder
```

## Rule 8: Use BuildKit features

Problem: Legacy builder misses useful optimizations and secure secret mounts.
Solution: Ensure BuildKit is enabled (new Docker enables it by default).
Reasoning: Better performance and modern Dockerfile features.
Example: `DOCKER_BUILDKIT=1 docker build .`

## Rule 9: Do not run app as root

Problem: Root in container is high-impact if container escape happens.
Solution: Create unprivileged user and switch with `USER`.
Reasoning: Least-privilege is a baseline hardening control.
Example:

```dockerfile
RUN addgroup -S app && adduser -S app -G app
COPY --chown=app:app . .
USER app
```

## Rule 10: Use Build Secrets, not `ARG`/`ENV`, for creds

Problem: `ARG`/`ENV` values can leak via layers/history.
Solution: Mount secrets at build time with BuildKit and consume in a single `RUN`.
Reasoning: Secret is ephemeral and not baked into final image/history.
Example:

```dockerfile
RUN --mount=type=secret,id=token \
    TOKEN="$(cat /run/secrets/token)" && \
    npm install
```

## Rule 11: Handle PID 1 and signals correctly

Problem: Shell wrappers often swallow `SIGTERM`; app gets `SIGKILL` from k8s later.
**Solution A:** Use `exec` in entrypoint script so app becomes PID 1.
**Solution B:** Use `tini` as init/entrypoint to forward signals and reap zombies.
Reasoning: Graceful shutdown protects in-flight requests and data integrity.
Example:

```bash
#!/bin/sh
exec node app.js
```

```dockerfile
# Setup tini
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "app.js"]
```

## Rule 12: Add `HEALTHCHECK`

Problem: "Process alive" is not equal to "service healthy". Cuz app may be in deadlock, connect lost or smth.
Solution: Probe a real health endpoint with timeout.
Reasoning: Orchestrator can stop routing to broken containers sooner.
Example:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -f http://localhost:8080/health || exit 1
```

## Rule 13: Lint Dockerfiles with Hadolint

Problem: Manual review misses common issues.
Solution: Run hadolint locally and in CI.
Reasoning: Fast static checks catch risky patterns early.
Example: `docker run --rm -i hadolint/hadolint < Dockerfile # In CI`
