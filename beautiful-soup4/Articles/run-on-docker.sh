docker build -t app-py .
docker run -it --name app-py-container app-py

rm -rf Articles/results
docker cp app-py-container:/Articles/results/ Articles/

docker rm app-py-container