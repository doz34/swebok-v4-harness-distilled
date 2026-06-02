# Refactoring Recipe
> Compiled from canonical works (Refactoring by Fowler, Tidy First? by Beck, Working Effectively with Legacy Code by Feathers)

## When to use
Improving the design of existing code without changing its behavior.

## Pre-requisites
- A solid test suite (characterization tests if working with legacy code)
- A version control system
- A willingness to commit small, atomic changes

## The 5-step process

### Step 1: Identify the smell
Common refactoring triggers:
- **Long method** (>20 lines, multiple levels of abstraction)
- **Long parameter list** (>3-4 params; group into object)
- **Duplicated code** (DRY violation)
- **Conditional complexity** (deeply nested if/else, switch on type)
- **Primitive obsession** (using strings/ints for domain concepts)
- **Data clumps** (groups of variables passed together)
- **Feature envy** (method uses another class's data more than its own)
- **Shotgun surgery** (one change requires changes in many places)
- **Refused bequest** (subclass doesn't use parent's methods)
- **Comments**: a comment explaining WHAT the code does often signals a missing method

### Step 2: Ensure tests exist
- Run the test suite — must be green before you start
- If no tests exist, write characterization tests first
- Tests should run in < 1 second for TDD cycle

### Step 3: Apply ONE refactoring at a time
The canonical list of refactorings (Fowler):

**Composing Methods**
- Extract Method
- Inline Method
- Extract Variable
- Inline Temp
- Replace Temp with Query
- Split Temporary Variable
- Remove Assignments to Parameters
- Replace Method with Method Object
- Substitute Algorithm

**Moving Features Between Objects**
- Move Method
- Move Field
- Extract Class
- Inline Class
- Hide Delegate
- Remove Middle Man
- Introduce Foreign Method
- Introduce Local Extension

**Organizing Data**
- Self Encapsulate Field
- Replace Data Value with Object
- Change Value to Reference
- Change Reference to Value
- Replace Array with Object
- Duplicate Observed Data
- Change Unidirectional Association to Bidirectional
- Change Bidirectional Association to Unidirectional
- Replace Magic Number with Symbolic Constant
- Encapsulate Field
- Encapsulate Collection
- Replace Record with Data Class
- Replace Type Code with Class
- Replace Type Code with Subclasses
- Replace Type Code with State/Strategy
- Replace Subclass with Fields

**Simplifying Conditional Logic**
- Decompose Conditional
- Consolidate Conditional Expression
- Replace Nested Conditional with Guard Clauses
- Replace Conditional with Polymorphism
- Remove Control Flag
- Replace Null Check with Null Object
- Introduce Assertion

**Simplifying Method Calls**
- Rename Method
- Add Parameter
- Remove Parameter
- Separate Query from Modifier
- Parameterize Method
- Replace Parameter with Explicit Methods
- Preserve Whole Object
- Replace Parameter with Method Call
- Introduce Parameter Object
- Remove Setting Method
- Hide Method
- Replace Constructor with Factory Method
- Encapsulate Downcast
- Replace Error Code with Exception
- Replace Exception with Test

**Dealing with Generalization**
- Pull Up Field
- Pull Up Method
- Pull Up Constructor Body
- Push Down Method
- Push Down Field
- Extract Subclass
- Extract Superclass
- Extract Interface
- Collapse Hierarchy
- Form Template Method
- Replace Inheritance with Delegation
- Replace Delegation with Inheritance

### Step 4: Run tests after each refactoring
- Red → Green → Refactor
- Tests must be green at every commit
- If a test fails, the refactoring was wrong; revert

### Step 5: Commit
- One refactoring per commit
- Clear commit message: "Extract Method: validateEmail from UserController.create"
- Reference the smell in the commit body

## Tidy First? (Kent Beck's approach)

Alternative to big refactoring sessions: **tidy before, during, or after each change** in small, safe steps.

Three timing choices:
1. **Tidy first** — refactor before adding the new feature
2. **Tidy along** — refactor as part of the feature
3. **Tidy after** — refactor after the feature is in

Guidance:
- Tidy first when the change would be hard to make cleanly
- Tidy along when small
- Tidy after when you don't know what shape the code will take

The book gives 30+ specific "tidying" operations, each safe to do independently.

## Refactoring legacy code (Feathers)

**The Legacy Code Change Algorithm:**
1. Identify change points
2. Find test points
3. Break dependencies
4. Write tests
5. Make changes and refactor

**Techniques for breaking dependencies:**
- **Sprout method**: wrap the legacy code in a new method you control
- **Sprout class**: wrap the legacy code in a new class
- **Wrap method**: keep the old method, delegate to a new one
- **Decoration**: use Decorator pattern to add behavior
- **Characterization tests**: tests that capture the CURRENT behavior, not the desired

**When you can't run tests:**
- Use a tool like Approval Tests to capture output
- Use log-and-replay for complex state
- Refactor in small steps, manually verify each

## Refactoring + AI assistance

Patterns that work well with AI pair programming:
- "Extract this block into a method named X"
- "Rename Y to Z and update all callers"
- "Replace this if-else chain with a polymorphism"
- "Add a guard clause for the null case"

Patterns to be careful with:
- "Rewrite this entire class" — too big, breaks atom
- "Optimize this" — often wrong without measurement
- "Add a comment explaining this" — often the code is just bad

## When NOT to refactor

- **No tests**: refactoring without tests is gambling
- **Right before a deadline**: schedule a separate refactoring sprint
- **Code that will be replaced soon**: don't polish a soon-to-be-deleted function
- **Code that is rarely changed**: ROI is low
- **Public APIs**: refactoring changes the contract

## Refactoring checklist

- [ ] Tests exist and are green
- [ ] Smallest possible change committed
- [ ] Tests still green after refactoring
- [ ] Behavior unchanged
- [ ] New design improves one of: readability, testability, extensibility, performance
- [ ] Commit message describes the refactoring and the smell

## Common mistakes

- **Refactoring AND feature in the same commit** (can't bisect, can't revert independently)
- **Big bang refactoring** (whole module in one PR — too risky)
- **"While I'm here"** scope creep
- **Forgetting to commit tests** (test drift from code)
- **Performance "refactoring"** without measurement (premature opt)
- **Refactoring for the sake of it** (some code is fine as-is)

## Related
- See `antipatterns.json` for the smells to look for
- See `checklists/p5-construction.md` for code quality gates
- See `recipes/code-review.md` for reviewing refactoring PRs
