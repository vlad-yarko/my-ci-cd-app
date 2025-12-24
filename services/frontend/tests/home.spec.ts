import { test, expect } from '@playwright/test'


test.describe('Home Page', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/')
	})

	test('should have correct metadata', async ({ page }) => {
		await expect(page).toHaveTitle('frontend')
	})

	test('should have correct elementes', async ({ page }) => {
		await expect(page.getByText('Anton').first()).toBeVisible()
	})
})
