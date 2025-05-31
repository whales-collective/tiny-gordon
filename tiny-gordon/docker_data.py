"""
🚧 work in progress
"""

docker_data = [
    {
        "input": "How do I run a container from an image?",
        "output": "docker run [OPTIONS] IMAGE [COMMAND] [ARG...]\nExample: docker run -d --name mycontainer nginx"
    },
    {
        "input": "How do I list all running containers?",
        "output": "docker ps\nFor all containers (including stopped): docker ps -a"
    },
    {
        "input": "How do I stop a running container?",
        "output": "docker stop CONTAINER_ID_OR_NAME\nExample: docker stop mycontainer"
    },
    {
        "input": "How do I start a stopped container?",
        "output": "docker start CONTAINER_ID_OR_NAME\nExample: docker start mycontainer"
    },
    {
        "input": "How do I remove a container?",
        "output": "docker rm [OPTIONS] CONTAINER [CONTAINER...]\nExample: docker rm mycontainer\nForce remove: docker rm -f mycontainer"
    },
    {
        "input": "How do I build an image from a Dockerfile?",
        "output": "docker build [OPTIONS] PATH | URL | -\nExample: docker build -t myimage:latest .\nWith build args: docker build --build-arg ARG_NAME=value -t myimage ."
    },
    {
        "input": "How do I list all images?",
        "output": "docker images\nOr: docker image ls\nShow all images including intermediate: docker images -a"
    },
    {
        "input": "How do I remove an image?",
        "output": "docker rmi [OPTIONS] IMAGE [IMAGE...]\nExample: docker rmi myimage:latest\nForce remove: docker rmi -f myimage"
    },
    {
        "input": "How do I pull an image from registry?",
        "output": "docker pull [OPTIONS] NAME[:TAG|@DIGEST]\nExample: docker pull nginx:latest\nFrom specific registry: docker pull registry.example.com/myimage"
    },
    {
        "input": "How do I push an image to registry?",
        "output": "docker push [OPTIONS] NAME[:TAG]\nExample: docker push myusername/myimage:latest\nPush all tags: docker push -a myusername/myimage"
    },
    {
        "input": "How do I execute a command in a running container?",
        "output": "docker exec [OPTIONS] CONTAINER COMMAND [ARG...]\nInteractive bash: docker exec -it mycontainer bash\nRun as root: docker exec -u root -it mycontainer bash"
    },
    {
        "input": "How do I view container logs?",
        "output": "docker logs [OPTIONS] CONTAINER\nFollow logs: docker logs -f mycontainer\nLast 100 lines: docker logs --tail 100 mycontainer\nWith timestamps: docker logs -t mycontainer"
    },
    {
        "input": "How do I copy files between container and host?",
        "output": "From host to container: docker cp /host/path CONTAINER:/container/path\nFrom container to host: docker cp CONTAINER:/container/path /host/path\nExample: docker cp myfile.txt mycontainer:/app/"
    },
    {
        "input": "How do I create a volume?",
        "output": "docker volume create [OPTIONS] [VOLUME]\nExample: docker volume create myvolume\nWith driver: docker volume create --driver local myvolume"
    },
    {
        "input": "How do I list volumes?",
        "output": "docker volume ls\nWith filter: docker volume ls --filter dangling=true"
    },
    {
        "input": "How do I remove volumes?",
        "output": "docker volume rm VOLUME [VOLUME...]\nExample: docker volume rm myvolume\nRemove unused volumes: docker volume prune"
    },
    {
        "input": "How do I create a network?",
        "output": "docker network create [OPTIONS] NETWORK\nExample: docker network create mynetwork\nWith subnet: docker network create --subnet=172.20.0.0/16 mynetwork"
    },
    {
        "input": "How do I list networks?",
        "output": "docker network ls\nShow detailed info: docker network inspect NETWORK_NAME"
    },
    {
        "input": "How do I run a container with port mapping?",
        "output": "docker run -p [HOST_PORT:]CONTAINER_PORT IMAGE\nExample: docker run -p 8080:80 nginx\nMultiple ports: docker run -p 8080:80 -p 3000:3000 myimage"
    },
    {
        "input": "How do I run a container with volume mount?",
        "output": "docker run -v /host/path:/container/path IMAGE\nNamed volume: docker run -v myvolume:/data IMAGE\nRead-only: docker run -v /host/path:/container/path:ro IMAGE"
    },
    {
        "input": "How do I run a container with environment variables?",
        "output": "docker run -e VAR_NAME=value IMAGE\nMultiple vars: docker run -e VAR1=value1 -e VAR2=value2 IMAGE\nFrom file: docker run --env-file .env IMAGE"
    },
    {
        "input": "How do I inspect a container or image?",
        "output": "docker inspect [OPTIONS] NAME|ID [NAME|ID...]\nContainer: docker inspect mycontainer\nImage: docker inspect myimage:latest\nFormat output: docker inspect --format='{{.State.Status}}' mycontainer"
    },
    {
        "input": "How do I tag an image?",
        "output": "docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]\nExample: docker tag myimage:latest myregistry/myimage:v1.0\nMultiple tags: docker tag myimage myimage:latest myimage:v1.0"
    },
    {
        "input": "How do I clean up Docker resources?",
        "output": "Remove stopped containers: docker container prune\nRemove unused images: docker image prune\nRemove unused volumes: docker volume prune\nRemove unused networks: docker network prune\nRemove everything: docker system prune -a"
    },
    {
        "input": "How do I run Docker Compose?",
        "output": "docker-compose up [OPTIONS] [SERVICE...]\nDetached mode: docker-compose up -d\nBuild before up: docker-compose up --build\nSpecific file: docker-compose -f docker-compose.yml up"
    },
    {
        "input": "How do I stop Docker Compose services?",
        "output": "docker-compose down [OPTIONS]\nRemove volumes: docker-compose down -v\nRemove images: docker-compose down --rmi all"
    },
    {
        "input": "How do I view Docker system information?",
        "output": "docker info\nSystem usage: docker system df\nReal-time events: docker events\nVersion info: docker version"
    },
    {
        "input": "How do I restart a container?",
        "output": "docker restart [OPTIONS] CONTAINER [CONTAINER...]\nExample: docker restart mycontainer\nWith timeout: docker restart -t 30 mycontainer"
    },
    {
        "input": "How do I pause/unpause a container?",
        "output": "Pause: docker pause CONTAINER\nUnpause: docker unpause CONTAINER\nExample: docker pause mycontainer && docker unpause mycontainer"
    },
    {
        "input": "How do I limit container resources?",
        "output": "docker run --memory=1g --cpus=1.5 IMAGE\nMemory limit: docker run -m 512m IMAGE\nCPU limit: docker run --cpus=0.5 IMAGE\nAll limits: docker run -m 1g --cpus=1 --memory-swap=2g IMAGE"
    }
]