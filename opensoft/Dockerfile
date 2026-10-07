# Use an official Node.js image as the base
FROM node:18-alpine AS builder

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the Next.js app
RUN npm run build

# --- Production stage ---
FROM node:18-alpine AS runner

WORKDIR /app

# Copy only the built output from the builder stage
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public

# Expose Next.js default port
EXPOSE 3000

# Run Next.js server in production mode
CMD ["npm", "run", "start"]
