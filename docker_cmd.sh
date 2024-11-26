# build
docker build -f Dockerfile_main -t tcdb-crawler-metadata .
docker build -f Dockerfile_image -t tcdb-crawler-image .



# run
docker run -e START_YEAR=2001 -e END_YEAR=2021 -e CATEGORY=Football my-python-app-2021