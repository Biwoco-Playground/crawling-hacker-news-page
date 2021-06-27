docker build -t app-py .
docker run -it --name app-py-container app-py

rm -rf justext/results
docker cp app-py-container:/justext/results/ justext/

docker rm app-py-container