import { expect, test } from '@playwright/test';

test('a member picks a court and sees it in the list', async ({ page }) => {
  await page.goto('/app/courts.html');
  await page.getByRole('button', { name: 'Pick court 2' }).click();
  await expect(page.getByRole('listitem').filter({ hasText: 'Court 2' })).toBeVisible();
});
