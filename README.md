### How to run it

Build a docker image

    docker build -t pokedex .

Run the image

    docker run -d -p 5000:5000 pokedex

The running server will be available on `http://localhost:5000`

### Documentation

You can access the documentation of the available endpoints here <http://localhost:5000/docs> or
here <http://localhost:5000/redoc>.

### What I'd do differently in production

- I'd add API versioning. The url would be in `/api/v1/pokemon` format.
- Optimally there would be some integrations tests, that actually call the endpoints of a deployed instance.
- I'd add proper logging.
- Setup certificates for https