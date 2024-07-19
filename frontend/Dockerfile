# build stage
FROM node:18.14.2 as build-stage
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . /app
RUN npm run build

# production stage
FROM node:18.14.2 as production-stage
WORKDIR /app
COPY --from=build-stage /app /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 3000
ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
