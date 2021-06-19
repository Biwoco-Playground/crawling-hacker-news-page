docker build -t app-py .
docker run -it --name app-py-container app-py

rm -rf app/src/results
docker cp app-py-container:/app/src/results/ app/src/

docker rm app-py-container