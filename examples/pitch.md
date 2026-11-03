# /pitch

Clamps the scope before writing code: states the ask, the smallest plan, and explicit non-goals before touching anything.

## Setup

The user asked to add a `--json` flag to `runExport()` in `src/export.js` so a script can consume the output instead of the formatted terminal table. The user ran `/pitch`.

```javascript
// src/export.js
export function runExport(data, options = {}) {
  const formatted = formatTable(data);
  console.log(formatted);
}
```

## Without /pitch

```text
I'll add the --json flag. To support multiple output formats cleanly, I created an OutputFormatter interface with TableFormatter and JsonFormatter implementations, added a FormatterFactory, added support for YAML and CSV export while we're here, updated cli.js to parse the new flags, and wrapped the JSON serialization in a custom replacer to handle BigInt and circular references.

Here are the 4 new files:
... [120 lines of scaffolding and new abstractions] ...
```

## With /pitch

```text
**Ask:** Add a `--json` flag to `runExport()` in `src/export.js` to output JSON instead of the terminal table.

**Smallest plan:** Check `options.json` in `src/export.js`. If set, print `JSON.stringify(data, null, 2)` and return before `formatTable(data)`.

**Won't do:** New formatter classes or interfaces, FormatterFactory, YAML/CSV formats, BigInt or circular reference replacers, CLI parsing changes, or touching `formatTable`.
```

```javascript
// src/export.js
export function runExport(data, options = {}) {
  if (options.json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }
  const formatted = formatTable(data);
  console.log(formatted);
}
```

## What changed

- The agent stops and states the pitch before writing or editing any code.
- Explicit **Won't do** items kill speculative abstractions (factories, unrequested formats, custom replacers) before they enter the diff.
- The implementation is 4 lines in the existing file instead of 4 new files and 120 lines of architecture.
