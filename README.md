## installing

#### clone repository
```sh
git clone git@github.com:danialsadri/BaseProject.git
```

#### change directory
```sh
cd BaseProject
```

#### config docker compose for development
```sh
docker compose -f docker-compose-development.yml up -d --build
```

#### config docker compose for production 
```sh
docker compose -f docker-compose-production.yml up -d --build
```
