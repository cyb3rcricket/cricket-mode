# Cricket Mode adapters

Adapters make the same Cricket behaviors available inside different coding-agent environments. They are intentionally thin.

## Adapter contract

An adapter may handle where instructions live, how commands are discovered/invoked, installation/update mechanics, tool wiring, and platform-specific limitations.

An adapter may **not** quietly change the meaning of a command.

The behavioral source of truth is `../core/COMMANDS.md`. Shared reply checks are `../conformance/`. The Cursor, Codex, and Antigravity checks call that module.

## Current targets

- `codex/` — implemented. Deterministic check passes. REQUIRES LIVE CODEX VALIDATION
- `cursor/` — implemented. Deterministic check passes. REQUIRES LIVE CURSOR VALIDATION
- `antigravity/` — implemented. Deterministic check passes. REQUIRES LIVE ANTIGRAVITY VALIDATION

More adapters can be added later without changing the portable core.

From this checkout, `python3 cricket install cursor|codex|antigravity --target /path/to/project` copies one adapter. See `docs/PORTABLE-CRICKET.md` for the files it writes and for the `.agents/skills` collision.

## Minimum bar for "implemented"

Do not mark an adapter complete until:

1. installation is documented,
2. all seven commands can be invoked or reliably requested,
3. all seven preserve the core contract,
4. conformance tests or transcripts exist,
5. known limitations are documented,
6. updates do not require hand-rewriting seven semantic copies.

Until then, label it **scaffold**, **experimental**, or **partial**.
