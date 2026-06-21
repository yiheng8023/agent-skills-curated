---
name: migrate-to-shoehorn
description: Replace unsafe `as` type assertions in TypeScript test files with type-safe alternatives. Use when user wants to replace `as` in tests, pass partial test data safely, or test with intentionally wrong types without losing autocomplete.
---

# TypeScript Test Type Safety — Replace `as` Assertions

## The problem with `as` in tests

Using `as Type` in tests is a common shortcut but creates real problems:

- Teams are trained not to use `as`, yet tests are full of it
- `as Type` hides missing required fields — tests pass even when the real code would fail
- `as unknown as Type` for intentionally wrong data loses autocomplete
- Tests become less trustworthy as a safety net

## Recommended approach: `@total-typescript/shoehorn`

The simplest drop-in replacement. Install once, replace assertions throughout.

```bash
npm i -D @total-typescript/shoehorn
# or: pnpm add -D / yarn add -D / bun add -D
```

### API

| Function | Use case |
|---|---|
| `fromPartial(obj)` | Pass partial data that still satisfies the type — missing fields are not required |
| `fromAny(obj)` | Pass intentionally wrong data (keeps autocomplete) |
| `fromExact(obj)` | Force full object — useful to swap in later for stricter coverage |

## Migration patterns

### Large objects — only some properties matter

**Before:**
```ts
getUser({
  body: { id: "123" },
  headers: {},
  cookies: {},
  // ...fake all 20 required properties
} as Request);
```

**After:**
```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as Type` → `fromPartial()`

```ts
// Before
getUser({ body: { id: "123" } } as Request);

// After
import { fromPartial } from "@total-typescript/shoehorn";
getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

```ts
// Before — intentionally wrong type for error-path testing
getUser({ body: { id: 123 } } as unknown as Request);

// After
import { fromAny } from "@total-typescript/shoehorn";
getUser(fromAny({ body: { id: 123 } }));
```

## Alternative libraries

If `shoehorn` is not suitable for your project, the same pattern can be achieved with:

- [`ts-jest`'s `mocked()`](https://jestjs.io/docs/jest-object#jestmockedsource-options) for mock objects
- Hand-rolled `fromPartial` helper: `const fromPartial = <T>(obj: Partial<T>) => obj as T;` (weaker, but zero-dependency)
- [`vitest`'s `vi.mocked()`](https://vitest.dev/api/vi.html#vi-mocked) for mocked modules

## Workflow

1. **Confirm scope** — ask the user:
   - Which test files or directories to migrate?
   - Are they dealing with large objects where only some fields matter?
   - Do they need to pass intentionally wrong data for error-path testing?

2. **Install** (if using shoehorn):
   ```bash
   npm i -D @total-typescript/shoehorn
   ```

3. **Find candidates:**
   ```bash
   grep -rn " as [A-Z]" --include="*.test.ts" --include="*.spec.ts" .
   grep -rn "as unknown as" --include="*.test.ts" --include="*.spec.ts" .
   ```

4. **Migrate** file by file:
   - Replace `as Type` → `fromPartial<Type>()` or chosen alternative
   - Replace `as unknown as Type` → `fromAny()` or chosen alternative
   - Add imports at top of each file

5. **Verify:**
   ```bash
   npx tsc --noEmit   # type check
   npm test           # run tests
   ```
