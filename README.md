# Pollen Engineering Test

## Introduction

Welcome to the Pollen code test. The test is broken into two parts

* Code Review
* Implementation

You are free to tackle the sections in any order. Please take as much or as little time
as you need in order to complete the test to your satisfaction. We recommend that test
should take a couple of hours (2-3) rather than days. All we ask is that you
let us know, truthfully, how much time you spent on the test. There is no right or wrong
amount of time, this info will simply help us with context when reviewing the results.

After you finish, please zip up the code (including the code review part) and email back. We review tests in an anonymised way so please don't include personal details in your submission.

## Setup

*Pre-requisites:*
- Python 3.6+

### Required dependencies

To install Python dependencies, run the following commands:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r ./requirements.txt

(cd ./ticketing && python manage.py migrate)
(cd ./recommendations && python manage.py migrate)
```

There are two Django projects here:

**`ticketing`**

- stores data about user's orders and runs an API that returns them
- you only need to review the code inside `ticketing`, you're not expected to make any changes
- to make testing easier you can run `setup_data` script (shown below) that it add example users, orders, and tickets to sqlite database
- you can run it by:
  ```
  cd ticketing
  python manage.py setup_data
  python manage.py runserver 3000
  ```
  which will make the server available at http://127.0.0.1:3000

**`recommendations`**

- it's where you need to add you implementation of the API, recommendations, and tests (it's empty at the moment)
- you can run it by:
  ```
  cd recommendations
  python manage.py runserver 4000
  ```
  which will make the server available at http://127.0.0.1:4000

We use pytest internally but you can choose the testing library you're most comfortable with.

You can run pytest tests with:

```
pytest
```

or unittest tests with:

```
python -m unittest
```

### Setting up test data

You can run `python manage.py setup_data` script that will add test data.

You can also add test data by yourself in shell, e.g.:

To run the shell in `ticketing` project:

```
python manage.py shell

from ticketing_api.models import User, Ticket, Order

User.objects.create(id=3, points=100)
ticket = Ticket.objects.create(id=3, price=100, reward_points=50)
order = Order.objects.create(user_id=3)
order.tickets.add(ticket)
```

then after starting the server with `python manage.py runserver 3000` you should be able to see the response after `curl http://127.0.0.1:3000/getOrders/1`


## Code review

We'd like you to code review everything inside the `./ticketing` Django project.

You can leave your feedback next to the code that it affects as a comment, e.g.
```
# Code Review: this will raise an exception
a = 1 / 0
```

Or, if you prefer, add your comments in `FEEDBACK.md`. Feel free to quote blocks of code in the markdown file or format it.

Treat this as a code review you'd provide to your colleague on a Github pull request. What we're looking for in this part:
- what you normally pay attention to when you're reviewing the code of your teammate
- how you communicate feedback to your colleagues
- what do you like about the code and what could be improved
- how you explain your various points and ideas for improvement (why? how?)
- apart from communication, we're looking for comments regarding the architecture of the existing solution, as well as performance, readability, and testing

## Implementation

We ask you to add code to this project that fulfills the objectives below. You can use the `recommendations` Django project for that.

You can assume this is a part of a larger ticketing system that enables users (we call them ambassadors) to sell tickets to their friends. For each sale they make (e.g. festival tickets) they receive a number of points. The more sales they make, the more points they collect and this allows them to choose rewards (such as free tickets or backstage access). Users are able to redeem the same type of rewards multiple times  (e.g. get 5 free drink vouchers for themselves and their friends).

The system exposes sales data (orders) in the API (`ticketing` project). The goal is to build a feature responsible for recommending rewards a user can get. The way the recommendation algorithm works is up to you.

Objectives:
- your implementation is expected to live inside the `recommendations` project (if you change anything in `ticketing` please explain your intent)
- write a client that consumes API endpoints defined in `ticketing` project
- add functionality that:
  - add a new API endpoint that returns recommendations for a user or an error if there are none
    - it could like similar to this:
    ```
    GET /recommendations/{userId} 
    
    {
        rewards: [
            ...
        ]
    }
    ```
    - multiple rewards of the same type can be recommended, e.g. if a user has 200 points, a reward for 100 points can be recommended twice
  - uses your API client to get user's orders
  - prepares recommendations for a user and saves them in the DB
  - this can be implemented in a script that would run regularly (see `recommendations/rewards/management/commands/refresh_recommendations.py`) for a simple example; execute `python manage.py refresh_recommendations` to run it
- we encourage adding tests to ensure your solution works as expected

Hints:
  - there is a list of available rewards (`rewards.py`) that can be recommended
  - every reward 'costs' a certain amount of points (detailed in `rewards.py`)
  - we have added an API client stub in `recommendations/rewards/ticketing_api_client.py` which you can expand
  - users get their rewards recommended based on how many points they've earned (stored in `User.points`)
  - every reward has a limit of how many times it can be recommended (`max_per_user` in `rewards.py`)
  - design of the recommendations algorithm is up to you, although please consider that meeting time constraints is more important than providing a sophisticated solution
  
Good luck!
