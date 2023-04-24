# Valorant Match Stats Crawler

We all love stats, don't we?

-----------

## Requirement
You need [Pipenv](https://pypi.org/project/pipenv/) and Python >=3.8 <br>
Or just see [this](./Pipfile) <br>
For dependency lock see [lock](./Pipfile.lock) <br>

-----------

## How to run
1. go to folder `Valorant.gg` <br>
2. run `pipenv` to enter Virtual Environment mode
3. run `python main.py {url} {filename}`

`url` and `filename` are optional. <br>
You need to define URL hard coded in the script, <br> for filename the default is `vlr_stats.csv`

-----------