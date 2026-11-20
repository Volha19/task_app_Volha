terraform{
    required_providers{
        docker = {
            source = "kreuzwerker/docker"
            version = "4.7.0"
             }
    }
}
provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_image" "tasks-api" {
  name  = "tasks-api"  
  build{
    context = "../services/tasks-api"
    tag =["tasks-api:local"]
    build_args = {
      foo : "zoo"
    }
    label = {
      author : "zoo"
    }
  }
}

resource "docker_image" "title-normilizer" {
  name  = "title-normilizer"  
  build{
    context = "../services/title-normilizer"
    tag =["title-normilizer:local"]
    build_args = {
      foo : "zoo"
    }
    label = {
      author : "zoo"
    }
  }
}

resource "docker_container" "tasks-api" {
  name = "title-normilizer"
  image = docker_image.tasks-tasks-api.image_id
  env = [
    "NORMALIZER_URL =http://${docker_container.normilizer.name}:5001" 
  ]
  ports {
    internal = 5001
    external = 5001
  }
}