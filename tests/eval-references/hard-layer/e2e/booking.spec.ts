import { expect, test } from '@playwright/test';

test('a member applies a coupon and sees the new court fee', async ({ page }) => {
  await page.goto('/app/booking.html');
  await page.getByLabel('Coupon code').fill('SPRING10');
  await page.getByRole('button', { name: 'Apply' }).click();
  await expect(page.getByLabel('Court fee')).toHaveText('$72.00');
});

test('a member sees why an expired coupon does not apply', async ({ page }) => {
  await page.goto('/app/booking.html');
  await page.getByLabel('Coupon code').fill('WINTER5');
  await page.getByRole('button', { name: 'Apply' }).click();
  await expect(page.getByRole('alert')).toHaveText('This coupon has expired.');
  await expect(page.getByLabel('Court fee')).toHaveText('$80.00');
});
