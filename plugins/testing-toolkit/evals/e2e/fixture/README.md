# notes-app

A small web app. `playwright.config.ts` holds the base URL. No E2E test exists yet.

## The journey that matters

A new visitor signs up and lands on their empty notebook. If this breaks, nobody can start using the product.

1. The visitor opens `/signup`.
2. They fill in "Email" and "Password", tick "I accept the terms", and press "Create account".
3. They land on `/notebook`, which shows the heading "Your notebook" and the text "No notes yet".

## Test helpers

The app exposes two helpers when it runs with `E2E=1`:

- `POST /api/test/users` with `{ "email": "...", "password": "..." }` creates a user directly.
- `DELETE /api/test/users/{email}` removes a user.

The markup of the sign-up page is in `app/signup.html`.
