---
name: test-e2e
description: "Writes end-to-end tests with Playwright for the few user journeys whose failure would be an incident, such as signup, login, checkout and the core workflow. Uses role and label locators, assertions that wait on their own, a fresh browser context per test, and data seeded through the API. Also covers accessibility checks and visual regression inside those journeys. Use for E2E tests, Playwright, browser tests, UI journey tests, flaky Playwright specs, or when the testing skill routes here. Not for component logic or business rules (use test-unit or test-integration)."
---

# End-to-end tests

An E2E test drives the real application through a browser. It is the slowest and most fragile kind of test, so it earns its place only on a journey whose failure would be an incident. Before you write one, name the journey. Move every check that is not part of that journey down to a unit or integration test, and say so to the user.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` for every test. This file adds the rules that are specific to E2E tests.

| Python | TypeScript / JS | JVM |
|---|---|---|
| Playwright Python | Playwright Test | Playwright Java |

## Five rules

1. **Locate elements by role and label.** Use `getByRole`, `getByLabel` and `getByText`, and use `getByTestId` only where no role or label exists. A locator that names what the user sees keeps working when the styling changes.
2. **Assert with web-first assertions.** `await expect(locator).toBeVisible()` waits until the condition holds. Never wait for a fixed time.
3. **Give every test a fresh browser context.** Each test signs in and builds its own state. No test depends on a test that ran before it.
4. **Seed data through the API.** Create the user, the cart or the order with a request in the test's setup. Use the UI only for the journey under test.
5. **Fail CI on a test that passes only on retry.** Keep retries on in CI for diagnosis, and set `failOnFlakyTests` so that a flaky test fails the run.

## Reject the test if

- It calls `waitForTimeout` or sleeps.
- It uses a CSS class or an XPath selector that depends on styling or DOM structure.
- It uses `describe.serial`, or one test relies on state from an earlier test.
- It signs in or seeds data through the UI in every test.

## Workflow

1. **Name the journey and its outcome.** Write the steps a user takes and the one outcome that proves the journey worked, such as "the order confirmation shows the order number".
2. **Apply step 0** of assured generation. The credible bug is a break in the journey: a button that no longer submits, a redirect that fails, a total that does not appear.
3. **Seed the data** in setup through the API, and sign in through stored state or an API call.
4. **Write the test** with role locators and web-first assertions. Assert the outcome of each step that matters, and the final outcome.
5. **Run it** with `npx playwright test --repeat-each=5 --retries=0`. When no browser is available, write the test and list the run under "Not run".
6. **Report** with the table from step 6 of assured generation.

## Accessibility and visual regression

Add an axe scan inside the journey for each page it visits, and fail on serious violations. For visual regression, take a screenshot only of a stable region, mask every dynamic value, and explain each baseline update in the PR.

## The report

End your reply with this table, even when you wrote one test. The user reads it to decide whether each row earns its place.

| Test | Journey and outcome it protects | Break that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```ts
// Bad. The selectors depend on styling, the wait is a fixed time, and the
// test relies on a user that an earlier test created through the UI.
test.describe.serial('checkout', () => {
  test('pays', async ({ page }) => {
    await page.click('.btn.btn-primary.checkout');
    await page.waitForTimeout(3000);
    expect(await page.locator('//div[3]/span').textContent()).toContain('Thanks');
  });
});
```

```ts
// Good. The test seeds its own cart through the API, locates by role and
// label, and waits on the assertion.
test('a signed-in customer can pay for a cart and sees the order number', async ({ page, request }) => {
  const cart = await request.post('/api/test/carts', { data: { sku: 'A1', qty: 2 } });
  expect(cart.ok()).toBeTruthy();

  await page.goto('/checkout');
  await page.getByLabel('Card number').fill('4242 4242 4242 4242');
  await page.getByRole('button', { name: 'Pay now' }).click();

  await expect(page.getByRole('heading', { name: 'Order confirmed' })).toBeVisible();
  await expect(page.getByText(/Order #\d+/)).toBeVisible();
});
```

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/strategy-models.md` | The user asks for E2E coverage of more than a few journeys |
