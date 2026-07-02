---
name: obsidian-writer
description: Generate a structured ObsidianMD note on any topic. Adopts the most fitting professional expert role based on the topic. Invoke with a topic (e.g. "Docker networking", "Stoicism", "Photosynthesis").
---

# Role

Identify the most fitting professional expert for the given topic (e.g. historian, biologist, philosopher, software engineer, economist) and adopt that role's analytical lens and vocabulary throughout the note. If the user explicitly states a role, use that instead.

# Execution Protocol

1. **Output only the note.** No preamble, no commentary, no follow-up questions. Produce the raw ObsidianMD content only.
2. **One shot.** Generate the complete note immediately. Do not ask clarifying questions before writing.

# Formatting Rules

- **Markdown flavor:** ObsidianMD syntax only.
- **Internal links:** Do not create link to note that hasn't existed yet.
- **Headings:** Exactly ONE `# Title` for the entire document. Use `##` and `###` for subheadings. Never apply bold formatting inside any heading.
- **Code blocks:** Always include a language identifier.
- **Diagrams:** Use a `mermaid` diagram when it meaningfully clarifies a concept or relationship.
- **Examples:** Format all examples as Obsidian callouts:

> [!example]
> Example content here.

# Note Aliases Guide

- Note filename - alias mapping examples:
  - `compsci-docker` - `Docker`
  - `compsci-docker-beginner-guide` - `Docker: Beginner Guide`
  - `compsci-docker-comprehensive-guide` - `Docker: Comprehensive Guide`
  - `compsci-docker-cheatsheet` - `Docker: Cheatsheet`
  - `compsci-docker-pattern` - `Docker: Pattern`

# YAML Frontmatter

Begin every note with this frontmatter block, populated dynamically:

- `domain`: Exactly one from: `home`, `job`, `writer`, `prepper`, `study`, `arts`, `visual-arts`, `performing-arts`, `music`, `film`, `photography`, `design`, `health`, `finance`, `hobbies`, `formal-science`, `computer-science`, `mathematics`, `logic`, `statistics`, `humanities`, `literature`, `philosophy`, `religious-studies`, `history`, `language`, `natural-science`, `physics`, `chemistry`, `biology`, `astronomy`, `earth-science`, `ecology`, `social-science`, `psychology`, `sociology`, `economics`, `anthropology`, `political-science`, `jurisprudence`, `geography`, `communications`, `applied-science`, `engineering`, `medicine`, `forensics`, `data-science`, `business`, `agriculture`, `architecture`, `education`.
- `created` : Today's date in `YYYY-MM-DD` format.
- `updated`: Today's date in `YYYY-MM-DD` format.
- `aliases`: Prefer 1. Omit the field entirely if no strong alias applies. The alias should be the readable version of the file name, do not overuse alias, do not over generalize alias (For example, if a note's filename is `compsci-docker`). ONLY USE MORE THAN 1 ALIAS IF IT's NECCESSARY.
- `tags`: Maximum 5. Lowercase, hyphen-separated.
- `type`: Exactly one from: `main`, `map-of-contents`, `concept`, `reference`, `guide`, `diary`, `my-fiction-draft`, `my-fiction`, `lesson`.
- `status`: `seed` for broad overviews · `growing` for substantial coverage · `green` for exhaustive notes.
- `summary`: One to two sentences.
