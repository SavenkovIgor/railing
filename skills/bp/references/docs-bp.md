# Documentation Validation

Evaluate documentation files for quality and effectiveness.
Verify that the documentation is up to date and accurately reflects the current state of the code.

## Evaluation Framework

### Key Documentation Principles

1. **Clarity**
   - Does the documentation use plain language that's easy to understand?
   - Are technical terms and acronyms properly defined or explained when first introduced?
   - Is the documentation accessible to the target audience?
   - Is the documentation grammatically correct?

2. **Conciseness**
   - Does the documentation focus on necessary information without overwhelming details?
   - Is each document focused on a specific topic or task?
   - Are edge cases appropriately handled without dominating the main content?

3. **Structure**
   - Is the documentation in proper, valid markdown format?
   - Is important information prioritized at the beginning?
   - Are headings used effectively to organize content and enable scanning?
   - Is text highlighting (bold, italics, code formatting) used judiciously (around 10% of text)?
   - Is styling consistent throughout the document and across related documents?
   - Do all file references use working markdown links?
   - Is all code naming formatted with inline `code` markdown?
   - Is terminology consistent throughout the document?

### Writing Style Rules

1. Remove bureaucratic and verbose phrases
   ❌ "For the purpose of increasing the efficiency of the system, a process of
       optimization is currently being conducted."
   ✅ "We are optimizing the system."

2. Prefer active voice over passive voice
   ❌ "The configuration file was modified to enable logging."
   ✅ "Modify the configuration file to enable logging."

3. Replace noun-based verbs with actual verbs
   ❌ "The execution of the installation can be performed by the administrator."
   ✅ "The administrator installs the software."

4. Be specific, avoid abstractions
   ❌ "The system provides a wide range of options for the user."
   ✅ "The system lets you export data to CSV, JSON, or XML."

5. Keep sentences short and clear
   ❌ "When the application encounters a situation in which the required
       library is missing, it will, in accordance with the predefined logic,
       generate an error message that informs the user about the problem."
   ✅ "If the library is missing, the app shows an error."

6. Cut filler and empty phrases
   ❌ "It should be noted that the installation process will take some time."
   ✅ "The installation takes several minutes."

7. Use verbs to make instructions actionable
   ❌ "The activation of the service is possible via the dashboard."
   ✅ "Activate the service in the dashboard."

8. Remove redundancy and duplication
   ❌ "Each and every user must always follow the mandatory rules."
   ✅ "Each user must follow the rules."

9. Address the reader directly ("you")
   ❌ "The feature can be used by the end user for configuration."
   ✅ "You can configure this feature."

10. Prefer present tense for clarity
    ❌ "The system was designed to support multiple platforms."
    ✅ "The system supports multiple platforms."

### Documentation Categories (Diátaxis Framework)

Assess whether the documentation provides adequate coverage across these categories:

1. **Tutorials** — Does it help developers learn and get started?
   - Are there step-by-step instructions for new contributors?
   - Do tutorials provide context and explain the "why" along with the "how"?

2. **How-to Guides** — Does it address specific tasks and goals?
   - Are there clear instructions for common development tasks?
   - Are the guides focused on practical outcomes?

3. **Explanation** — Does it provide understanding of concepts and architecture?
   - Is there documentation explaining the project's structure and design decisions?
   - Are relationships between components clearly explained?

4. **Reference** — Does it provide technical specifications?
   - Is API documentation clear and complete?
   - Are configuration options documented?
