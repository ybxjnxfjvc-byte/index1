const { test, expect } = require('@playwright/test');

const base = process.env.CASE_BASE_URL || 'https://ybxjnxfjvc-byte.github.io/index1/';

test('trainer treats participant input as text and does not submit results by default', async ({ page }) => {
  const requests = [];
  page.on('request', request => {
    if (request.method() !== 'GET') requests.push(request.url());
  });

  await page.goto(new URL('03_trenazher_kross_prodazh_sber.html', base).toString());
  const payload = '<img src=x onerror=alert(1)>';
  await page.locator('#name').fill(payload);
  await page.locator('#unit').fill('demo unit');
  await page.locator('#begin').click();

  await expect(page.locator('#hello')).toContainText(payload);
  await expect(page.locator('#hello img')).toHaveCount(0);

  for (let i = 0; i < 10; i++) {
    const answers = page.locator('.answer');
    await answers.first().click();
    await page.locator('#next').click();
  }

  await expect(page.locator('#result')).toHaveClass(/active/);
  await expect(page.locator('#sumName')).toHaveText(payload);
  expect(requests).toEqual([]);
});

test('main lesson exposes keyboard skip link', async ({ page }) => {
  await page.goto(base);
  await page.keyboard.press('Tab');
  await expect(page.locator('.skip')).toBeFocused();
});
