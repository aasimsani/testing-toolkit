# profile-widget

A small frontend module. It shows a user's name, avatar and plan badge. It gets them from the `users-api` service, which another team owns.

`src/usersClient.js` is the only code that calls `users-api`. `docs/user-response.json` is a sample of what `GET /users/{id}` returns today.

The two teams have broken each other twice this quarter, so this repo needs a consumer-driven contract test with Pact. `@pact-foundation/pact` and `vitest` are in `package.json`. The pact broker is at `$PACT_BROKER_BASE_URL`.
