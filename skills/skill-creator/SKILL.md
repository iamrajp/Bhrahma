---
name: skill-creator
description: Create new skills by learning from the internet. Use this skill when the user requests a new capability that doesn't exist yet, or when you need to learn how to do something new. This skill searches the web, extracts documentation, and generates a new SKILL.md file.
category: meta
tags: learning, skill-creation, web-search
---

# Skill Creator

You are now using the skill-creator skill to learn and create new capabilities.

## When to Use This Skill

Use this skill when:
- The user explicitly asks to "learn" or "create a skill"
- You need a capability that doesn't exist in the current skill set
- The task requires specialized knowledge not in your training data
- You need up-to-date information about a technology or framework

## Skill Creation Process

### 1. Interview the User

Ask clarifying questions to understand:
- What functionality is needed?
- When should this skill be triggered?
- What should the output format be?
- Are there specific requirements or constraints?

### 2. Research from the Internet

Use web search to gather information:
- Search for official documentation
- Look for tutorials and guides
- Find code examples and best practices
- Check Stack Overflow and GitHub for practical usage

Focus on authoritative sources:
- Official documentation sites
- GitHub repositories
- Well-known tech blogs and tutorials
- Stack Overflow accepted answers

### 3. Extract and Synthesize Knowledge

From the research:
- Identify key concepts and patterns
- Extract step-by-step procedures
- Collect code examples and templates
- Note common pitfalls and best practices

### 4. Generate SKILL.md

Create a SKILL.md file with:

**Frontmatter (YAML)**:
```yaml
---
name: skill-name-in-kebab-case
description: Clear description of what the skill does AND when to use it (be specific and "pushy" about triggering conditions)
category: appropriate-category
tags: relevant, tags, here
---
```

**Instructions (Markdown)**:
- Clear, step-by-step instructions
- Explain the "why" behind each step, not just rigid rules
- Include examples and code snippets
- Keep under 500 lines total
- Use progressive disclosure (put detailed info in bundled resources if needed)

### 5. Test the Skill (if applicable)

For objective skills (file transforms, code generation):
- Create test cases
- Verify expected outputs
- Test edge cases

For subjective skills (writing styles, creativity):
- Review examples
- Verify consistency with requirements

### 6. Optimize the Description

The description is critical for skill triggering. Make it:
- Specific about what the skill does
- Clear about when to use it
- "Pushy" about triggering conditions (Claude tends to under-trigger skills)
- Include keywords that match common user queries

**Good Description Example**:
"Generate Python unit tests using pytest. Use this skill whenever the user asks to test Python code, create tests, add test coverage, or verify functionality. Works with functions, classes, and modules."

**Bad Description Example**:
"Helps with testing" (too vague, won't trigger reliably)

## Best Practices

1. **Keep Skills Focused**: One skill = one clear purpose
2. **Explain Reasoning**: Don't use "ALWAYS" or "NEVER" - explain why something should be done
3. **Progressive Disclosure**: Put complex details in separate resource files
4. **Make Descriptions Pushy**: Over-specify when to use the skill
5. **Test Before Saving**: Verify the skill works as expected
6. **Generalize from Examples**: Don't overfit to specific test cases

## Example Skill Structure

```
skill-name/
├── SKILL.md (required)
├── scripts/
│   └── helper-script.py
├── references/
│   └── api-docs.md
└── assets/
    └── template.txt
```

## Output Format

After creating the skill:
1. Show the SKILL.md content
2. Explain what the skill does
3. Describe when it will be triggered
4. Save it to the skills database
5. Confirm it's ready to use

## Important Notes

- Search multiple sources to get comprehensive information
- Prefer official documentation over third-party tutorials
- Test skills with edge cases when possible
- Update skill descriptions based on actual triggering patterns
- Keep the skill focused - don't try to do too much in one skill
