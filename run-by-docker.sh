docker build -t app-py .
docker run -it --name app-py-container app-py

rm -r results && mkdir results
docker cp app-py-container:/app/src/compiling-time.txt results
docker cp app-py-container:/app/src/beautifulSoup4.txt results

docker rm app-py-container