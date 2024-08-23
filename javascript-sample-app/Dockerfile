
# build stage
FROM node:22 AS builder

WORKDIR /usr/src/app

# No need to copy package.json and package-lock.json as they are bind-mounted
#COPY package*.json ./

# Install dependencies.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev

# Copy the source code of the application
COPY . .

# execution stage
FROM gcr.io/distroless/nodejs22-debian12

# Copy the application directory from the build stage
COPY --chown=nonroot:nonroot --from=builder /usr/src/app /usr/src/app
USER nonroot

WORKDIR /usr/src/app
CMD [ "index.js" ]
