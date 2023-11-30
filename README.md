# 🚚 FeastFinder: Your Gateway to San Francisco's Food Truck Delights! 🌯🍔

![Build Status](https://github.com/RustamGarayev/food_truck_finder/actions/workflows/docker-image.yml/badge.svg?branch=main)
![Python Version](https://img.shields.io/badge/python-3.10-blue)
![Github last-commit](https://img.shields.io/github/last-commit/RustamGarayev/food_truck_finder)

## Overview
Hey there, fellow foodies!
Are you ready to embark on a tantalizing journey through the bustling streets of San Francisco, in search of the finest food trucks the city has to offer?
FeastFinder is here to guide you through this culinary adventure!
Built with love (and a little bit of code), this application is your ultimate companion in discovering mouth-watering street food gems.

## Table of Contents
- [Getting Started](#getting-started)
- [What's cooking?](#whats-cooking)
- [Database Population from CSV](#database-population-from-csv)
- [Usage](#usage)
- [Further Improvements](#further-improvements)

## Getting Started
Fire up your engines (or your laptops)!

All you need to get started is a working installation of [Docker](https://docs.docker.com/get-docker/).
No complicated setup, no fuss - just pure, unadulterated food truck fun with a simple command!

```bash
$ docker-compose up --build
```

> But what about database? And migrations? And dependencies? And population?

Don't worry, we've got you covered!

Once the build is done, you can access the application at [localhost](http://0.0.0.0:8000/) port 8000.

[API documentation](http://0.0.0.0:8000/docs/) will also be available.

## What's cooking?
* [Django REST Framework](https://github.com/encode/django-rest-framework): The backbone of our application.
* [Docker](https://docs.docker.com/): The secret ingredient to our seamless development and deployment process.
* [Swagger UI](https://swagger.io/tools/swagger-ui/): Makes exploring the API as enjoyable as browsing a food menu.
* [Pre-commit Hooks](https://pre-commit.com/): Keeps our codebase clean, because no one likes messy code (or kitchens).
* [Poetry](https://github.com/python-poetry/poetry): Our dependency manager of choice.
* [Postgis](https://postgis.net/): The database that stores all our food truck data.

## Database Population from CSV
FeastFinder leverages Django's powerful ORM capabilities to populate its database with the San Francisco food truck data. Here's how it works:

- **Data Import Script**: Django management command called `populate_database` is used to process the CSV file when the image is built for the first time.
- **Handling Geospatial Data**: Overwrite the `save()` method of the `FoodTruck` model to save the `point_location` field from the float values to a `Point` object.
- **Migrations**: Standard Django migrations are used to manage the database schema. Whenever the models are modified, a new migration is created and applied to the database when the container is run.

## Usage
FeastFinder is a simple, intuitive application that's easy to use.

* Find a Truck: Enter your current location (either IP or lat/lgt) or just let your device tell us where you're at.
* Set Your Appetite: Tell us how many trucks you want to choose from.
* Discover: Hit 'Find Food Trucks' and voilà! A list of nearby food havens appears.

*PS: I know the UI is awesome, don't ask me how I did it. 😉*

## Further Improvements
* Add unit/integration tests to ensure code quality and prevent regressions.
* Add authentication and authorization to the API. For now, the API is open to the public.
