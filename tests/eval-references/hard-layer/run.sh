# The run passes, and the test of the exact minimum is reported as a failing todo.
out="$(node --test --test-reporter=tap "src/**/*.test.js")" && grep -q '^not ok .* # TODO' <<<"$out"
