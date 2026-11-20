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
    tag =["tasks-api:local
    ]
    build_args = {

    }
  }

resource "docker_image" "title-normilizer" {
  name  = "title-normilizer"  
  image = "title-normilizer:local"
  ports {
    internal = 5001
    external = 8000
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