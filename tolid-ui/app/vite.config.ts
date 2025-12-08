/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import viteTsconfigPaths from "vite-tsconfig-paths";
import fs from "fs";
import basicSsl from '@vitejs/plugin-basic-ssl'

// Paths to the key and certificate files
const keyPath = "/localhost.key";
const certPath = "/localhost.crt";

// Check if both the key and certificate files exist
const httpsConfig =
  fs.existsSync(keyPath) && fs.existsSync(certPath)
    ? {
        key: fs.readFileSync(keyPath),
        cert: fs.readFileSync(certPath),
      }
    : false;

export default defineConfig({
  plugins: [react(), viteTsconfigPaths(),basicSsl()],
  build: {
    emptyOutDir: true,
    outDir: "build",
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    https: true
  }
});
