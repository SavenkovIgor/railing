# DevOps best practices

## Best practices

Infrastructure as Code (IaC): The practice of managing and provisioning
infrastructure through git repositories and code, rather than manual configuration.

If the project uses IaC, use IaC instead of manual configuration, even for small tasks. Then every change is tracked and can be rolled back.

Idempotency: an important property of scripts and tools. Repeated execution
produces the same result, regardless of the current state of the system.

Split responsibilities:

- Provisioning (resource creation): hardware, network, storage, balancers.
  Terraform is a common tool for this.
- Configuration management (software installation and configuration): nginx, databases, applications.
  Ansible is a common tool for this.

### Difference between declarative and scripting approaches

- Declarative approach: Define the desired state of the infrastructure
- Scripting approach: Define the steps to achieve the desired state

## Antipatterns

ClickOps: The practice of using a click-based interface to perform operations
tasks, instead of command-line tools or scripts.
It is slow, unreliable, and undocumented.
