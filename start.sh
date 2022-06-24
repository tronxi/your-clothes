docker rm clothes -f
docker run -v ${PWD}/armario:/armario/ -ti --name clothes clothes