# Multi-stage build for React frontend
# Build stage
FROM node:18-alpine AS build
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --legacy-peer-deps

# Copy source and build
COPY . .
RUN npm run build

# Production stage - serve with nginx
FROM nginx:stable-alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Replace default nginx config with our SPA-friendly config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
