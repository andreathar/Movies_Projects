# React Compiler Report - Failures

## Instructions

The following components failed to be optimized by the React Compiler. Fix each function one by one so the compiler can successfully memoize them.

**Rules:**
- Do not change the underlying logic or behavior of any component.
- Preserve the existing API (props, return values, side effects).
- If a fix requires restructuring, extract helper functions rather than rewriting the component.
- If a failure reason is ambiguous or the fix is unclear, ask for clarification before making changes.

---

> Generated: 10/12/2026, 11:44:52 PM
> Total failed components: 5

## sites/movies-demandas/app/dashboard.tsx

- **dashboard** (line 48): (BuildHIR::lowerStatement) Handle TryStatement with a finalizer ('finally') clause
- **dashboard** (line 54): (BuildHIR::lowerStatement) Support ThrowStatement inside of try/catch
- **dashboard** (line 54): (BuildHIR::lowerStatement) Support ThrowStatement inside of try/catch

## sites/movies-demandas/components/ui/calendar.tsx

- **calendar** (line 37): (BuildHIR::lowerExpression) Handle tagged template where cooked value is different from raw value
- **calendar** (line 38): (BuildHIR::lowerExpression) Handle tagged template where cooked value is different from raw value
