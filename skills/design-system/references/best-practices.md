# Design System Best Practices

## Foundations

1. 4-unit spacing grid - all paddings, gaps, margins, and sizes must be multiples of 4 (4, 8, 12, 16, 24, 32, 48, 64). No arbitrary values.
2. Semantic color names - `color-surface`, `color-text-primary`, not `gray-100`. Raw literals in components break refactoring.
3. Limit the palette - 2–3 background layers, 2–3 surface levels, one set of semantic role colors (error, warning, success, info, neutral), plus brand/accent.
4. Minimum interactive target - 48 units for touch, 24 units for pointer.

## Typography

1. One typeface family - multiple weights (light/regular/bold) are enough for hierarchy. Add a second only for a distinct role (e.g., monospace for code). Never more than two.
2. One role per typeface - two families for body copy = incoherent system.
3. Type scale mirrors the spacing grid - steps: 12, 14, 16, 20, 24, 32. Line-height: unitless ratio (1.2, 1.4, 1.6), not fixed px.
4. Limit the number of available type styles - define heading, subheading, body, caption, label. No ad-hoc sizes in code outside the predefined set.

## Tokens

1. Three-layer hierarchy - primitive tokens (raw values) → semantic tokens (`color-error = red-500`) → component tokens (`button-bg-error = color-error`). Components reference only semantic or component tokens, never primitives.
2. Tokens everywhere, literals nowhere - never write a raw color or size directly in a component outside the token definition.
3. Token naming: role > category > variant - `color-node-concept`, `spacing-card-padding`, `radius-card`. Avoid positional names (`color-1`) and pure visual names (`blue-500`).
4. One source of truth for tokens - one file or module. Fragmented token definitions lead to drift.
5. Semantic tokens exist to enable theming - switching a theme (light/dark, brand variant) should require changing token values only, not component code.

## Components

1. Document all states - every interactive component requires: default, hover/focus, active/selected, disabled, and (if applicable) loading and error. Missing states invite inconsistent ad-hoc solutions.
2. Semantic variants over visual variants - name by meaning (`type: "warning"`) not appearance (`color: "yellow"`). Visual decisions belong in the token, not the variant name.
3. One source of truth for anatomy - if DESIGN.md says card padding is `16 units`, the component must reference the `spacing-card-padding` token. Any divergence is a bug, not a style preference.

## Documentation

1. Single `DESIGN.md` per project - do not fragment the spec across multiple docs. One file, updated in-place, is the source of truth for humans and agents alike.
