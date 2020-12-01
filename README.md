
## About The Project
> Kopernik. The backend for pizza ordering system.

![](kopernik.gif)


### Built With
-   Django
-   Django REST Framework
-   Python
-   PostgreSQL

### Prerequisites
-   Docker 19.03
-   docker-compose 1.27

## Installation

 1. Clone the kopernik ```git clone https://github.com/gedomer/kopernik.git```

 2. Copy example env file in ```"config/"``` into root of project as .env.
 3. Run ```docker-compose up```

 4. Create initial data: ```docker-compose run web python manage.py loaddata fixtures/kopernik.json```
     (You can reset the database with  `docker-compose exec web python manage.py flush`).
 5. Default admin app credentials: "admin:admin"

### Commands

 - To shut down the Docker containers: ```docker-compose down```

### Run tests

 Run ```docker-compose run web python manage.py test```


## Documentations
* [API Endpoints](https://github.com/gedomer/kopernik/blob/main/docs/api.md)

 
## Release History
* 0.0.1
* Work in progress

## Meta
- gedomer – [@gedomer](https://github.com/gedomer)
- Distributed under the MIT license. See ``LICENSE`` for more information.