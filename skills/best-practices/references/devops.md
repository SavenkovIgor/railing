# DevOps best practices

## Best practices

Infrastructure as Code (IaC): The practice of managing and provisioning
infrastructure through git repositories and code, rather than manual configuration.

If you start work with IaC, you should always use IaC instead of manual configuration, even for small tasks. This ensures that all changes are tracked and can be easily rolled back if necessary.

Idempotency: important property of scripts and tools, meaning that repeated
execution will always produce the same result, regardless of the current state of the system.

Split responsibilities:

- Provisioning (resource creation): hardware, network, storage, balancers.
  Terraform is a common tool for this
- Configuration management (software install & config): nginx, databases, applications etc.
  Ansible is a common tool for this

### Difference between declarative and scripting approaches

- Declarative approach: Define the desired state of the infrastructure
- Scripting approach: Define the steps to achieve the desired state

## Antipatterns

ClickOps: The practice of using a click-based interface to perform operations
tasks, instead of using command-line tools or scripts.
It is long, unreliable and undocumented
