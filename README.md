# 🦗 Cricket Mode!

Small, focused agent skills for working better with coding agents.

Cricket Mode adds a handful of slash-command behaviors for common moments in AI-assisted development: simplify an explanation, teach the code that was just written, challenge an implementation, prove that something actually works, or find where a project has drifted out of sync.

Each skill does one thing.

## Skills

| Command | What it does |
| --- | --- |
| `/chirp` | Makes the last explanation simpler, shorter, and easier to understand. |
| `/senpai` | Teaches you what the agent just built, how it works, why it was done that way, and the reusable pattern behind it. |
| `/challenge` | Tries to break the work before you trust it. Looks for bugs, weak assumptions, edge cases, and unintended behavior. |
| `/prove-it` | Verifies the real behavior and shows evidence instead of merely claiming the work is correct. |
| `/drift` | Finds places where the project no longer agrees with itself, such as code vs. tests, docs vs. behavior, or config vs. reality. |

## Why Cricket Mode?

Coding agents are good at producing a lot of work quickly.

That creates a few recurring problems:

- explanations get dense,
- generated code can be hard to learn from,
- plausible-looking implementations can hide mistakes,
- passing code can still fail in the real application,
- and fast-moving repositories can slowly contradict themselves.

Cricket Mode gives each of those moments a simple command.

```text
/chirp      Make the last answer click.
/senpai     Teach me what you just built.
/challenge  Try to break it before we trust it.
/prove-it   Don't tell me it works. Prove it.
/drift      Find where the project disagrees with itself.
```

## Installation

Copy any skill you want from:

```text
.agents/skills/
```

into the `.agents/skills/` directory of your project.

For example:

```text
your-project/
└── .agents/
    └── skills/
        ├── chirp/
        │   └── SKILL.md
        └── prove-it/
            └── SKILL.md
```

You can install only the skills you want.

## Usage

After the skills are available to your coding agent, invoke them directly:

```text
/chirp
```

```text
/senpai
```

```text
/challenge
```

```text
/prove-it
```

```text
/drift
```

The commands are intentionally small. They are meant to change how the agent approaches a task, not introduce a giant workflow framework.

## Examples

Annotated before/after transcripts in [`examples/`](examples/) are proof that each skill changes what the agent says and does.

## Philosophy

Start with the smallest instruction that reliably changes behavior.

A skill should have one clear job.

Add complexity only when real use proves that it is needed.

## Status

Cricket Mode is early and experimental.

The current skills are being tested through real AI-assisted development workflows and will change as useful failure cases show up.

## License

MIT