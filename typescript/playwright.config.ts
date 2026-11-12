import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  use: { baseURL: "http://127.0.0.1:5000" },
  webServer: {
    command: "python ../app/app_fastapi.py",
    url: "http://127.0.0.1:5000",
    reuseExistingServer: true,
  },
});
