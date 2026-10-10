---
name: design-system
description: >-
  You should use this skill when: designing or auditing a design system;
  extracting design tokens from code; validating design tokens and UI consistency;
  reviewing implementation against spec; ensuring design best practices.
---

# Design System Skill

## Procedure

### Mode: Create `DESIGN.md`

1. Explore the project - read existing UI files to extract conventions.
   - CSS/SCSS, Tailwind config, component files, constants, tokens
   - If none exist, ask the user for their intent.
2. Extract foundations from code or the user's description:
   - Spacing scale (base unit and multiples)
   - Color palette: backgrounds, surfaces, borders, text roles, semantic colors
   - Typography: families, weights, sizes, line-heights
   - Shape: border-radius, shadows, z-index
3. Document components - for each reusable UI component, record:
   - Visual anatomy (background, border, icons)
   - All states: default, hover, active, disabled, loading, error
   - Variants keyed by semantic role, not appearance
4. Document interactions - transitions, animation durations, zoom/scale behavior
5. Write `DESIGN.md` using the [template](assets/DESIGN.md.template) at project root or `docs/`.
6. Define design tokens - create a token file (`tokens.css`, Tailwind, or JS) replacing all raw values with names.
7. Validate the draft - trace every value in `DESIGN.md` to code or design decision. Flag assumptions.

### Mode: Audit Project

1. Read `DESIGN.md` - load the current design spec.
2. Scan UI source files for:
   - Hex/rgba color literals outside token file
   - Pixel sizes not in spacing scale
   - Font sizes/weights not in typography scale
   - Border-radius/shadow values not in shape scale
3. Classify findings:
   - 🔴 Critical - contradicts DESIGN.md (wrong color or spacing)
   - 🟡 Token opportunity - matches DESIGN.md but is raw literal
   - 🔵 Undocumented - consistent but not in DESIGN.md
4. Report findings prioritized by severity.
5. Fix - replace raw literals with tokens after user confirms.

### Mode: Update `DESIGN.md`

1. Identify changes: new component, added color, interaction pattern.
2. Edit only affected sections; don't restructure.
3. Additive changes are always safe.
4. Mark breaking changes with `> ⚠️ Breaking:` and migration path.

## Best Practices Reference

See [Design System Best Practices](references/best-practices.md) for foundational principles to apply when creating or reviewing any design system.

## Output Checklist

- [ ] `DESIGN.md` placed at project root or `docs/`
- [ ] All foundations documented: spacing, color roles, typography, radius, shadows
- [ ] Every semantic color has a name (not just a hex value)
- [ ] All reusable components documented with all interactive states
- [ ] Design tokens defined (CSS variables, JS constants, or Tailwind theme)
- [ ] Interactions documented: hover, active, transitions, zoom breakpoints
- [ ] Audit findings prioritized: 🔴 Critical → 🟡 Token opportunities → 🔵 Undocumented
