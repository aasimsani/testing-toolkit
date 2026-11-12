import { expect, test } from '@playwright/test';

test('a shopper adds an item and sees it in the cart', async ({ page }) => {
  await page.goto('/app/cart.html');
  await page.getByRole('button', { name: 'Add tea towel' }).click();
  await expect(page.getByRole('listitem').filter({ hasText: 'Tea towel' })).toBeVisible();
});
