# ZARSPREAD

The Luno South African BTC exchange often has BTC priced higher than on international USD exchanges.
This is a small django project to track that price difference. I use Celery to handle scheduling of
regular price updates and Redis as a message broker.

The App can be found here hosted on a single Heroku dyno: https://checkthespread.herokuapp.com
