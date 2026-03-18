FROM node:20-alpine AS build

WORKDIR /app

# Ensure devDependencies are installed for tsc/vite build
ENV NODE_ENV=development

# Build-time env for Vite (import.meta.env.VITE_*)
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# pnpm via corepack
RUN corepack enable
RUN pnpm config set node-linker hoisted

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build


FROM nginx:alpine AS serve

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
