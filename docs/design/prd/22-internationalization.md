# 22 — Internationalization Plan

> Sub-document of the [Design overview](../README.md). Beyond "multi-language artifacts" — full UI/report localization, model language coverage, and cultural calibration of disagreement vocabulary.

## 22.1 Three layers of i18n

| Layer | What | v0.1.0 | v0.5.0 | v1.0.0 |
|-------|------|--------|--------|--------|
| **Artifact language** | The artifact under review can be in any language | ✅ (model-dependent) | ✅ | ✅ |
| **Report language** | The verdict/disagreement report output language | English only | 5 languages | 10+ languages |
| **UI language** | The side-by-side review interface | English only | 3 languages | 5+ languages |

## 22.2 Artifact language handling

- The engine is language-agnostic: it passes artifact content to the reviewer model as-is. If the model understands Japanese contracts, the engine processes Japanese contracts.
- **No translation layer** — translating artifacts before review introduces translation errors that masquerade as review findings. The artifact is reviewed in its original language.
- The `ReviewArtifact` schema includes a `detected_language` field (auto-detected, overridable) so reports can state what language the artifact was in.

## 22.3 Report localization (v0.5.0+)

Reports are generated in the artifact's detected language by default. Override via `--report-language <code>`.

**Localization challenges specific to debate:**

| Challenge | Why it matters | Approach |
|-----------|---------------|----------|
| Disagreement vocabulary | "Disputed" vs "contested" vs "未決" carry different connotations | Domain-specific glossary per language; reviewed by native speakers before shipping |
| `would_resolve_if` phrasing | Must sound actionable, not hedged, in every language | Template-based generation with locale-specific action verbs |
| Evidence references | "See line 42" vs "42行目を参照" — formatting differs | ICU MessageFormat for all template strings |
| Severity labels | "High/Medium/Low" map differently across risk cultures | Configurable severity scale per locale (e.g., Japanese: 高/中/低) |

## 22.4 Model language coverage matrix

The engine doesn't guarantee language support — the *model* does. Documentation includes a community-maintained matrix:

| Model family | English | Spanish | Japanese | German | Chinese | Arabic |
|-------------|---------|---------|----------|--------|---------|--------|
| GPT-4o | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude 3.5 | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Llama 3 | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| Qwen 2 | ✅ | ⚠️ | ✅ | ❌ | ✅ | ⚠️ |

Users check this matrix before configuring a reviewer pair for non-English artifacts. Heterogeneous pairs must both support the artifact's language.

## 22.5 Cultural calibration

Disagreement norms differ across cultures. A direct objection ("This claim is wrong because...") is normal in German engineering review but may be too blunt in Japanese business contexts.

- v0.5.0: `--disagreement-style` flag (`direct` | `diplomatic` | `formal`) adjusts objection phrasing in the reviewer prompt
- This is a *prompt-layer* concern, not an engine-layer concern — the engine produces the same structured `Objection` objects regardless of style
- Style affects the *presentation* of objections in reports, not the *detection* of disagreements
