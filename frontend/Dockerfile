FROM node:20-slim AS base
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM base AS runner
COPY --from=build /app/dist ./dist
RUN pnpm add serve
EXPOSE 4321
CMD ["pnpm", "serve", "dist", "-l", "4321"]
