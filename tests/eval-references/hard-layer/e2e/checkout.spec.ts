import { expect, test } from '@playwright/test';

test('a shopper applies a coupon and sees the new total', async ({ page }) => {
  await page.goto('/app/checkout.html');
  await page.getByLabel('Coupon code').fill('SPRING10');
  await page.getByRole('button', { name: 'Apply' }).click();
  await expect(page.getByLabel('Total')).toHaveText('$72.00');
});

test('a shopper sees why an expired coupon does not apply', async ({ page }) => {
  await page.goto('/app/checkout.html');
  await page.getByLabel('Coupon code').fill('WINTER5');
  await page.getByRole('button', { name: 'Apply' }).click();
  await expect(page.getByRole('alert')).toHaveText('This coupon has expired.');
  await expect(page.getByLabel('Total')).toHaveText('$80.00');
});
