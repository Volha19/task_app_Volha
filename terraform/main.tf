terraform{
    required_providers{
        docker = {
            source = "kreuzwerker/docker"
            version = "4.7.0"
             }
    }
}
provider "docker" {}
resource "docker_image" "web"{
    name = "nginx:1.31.9"
}

resource "docker_container" "web" {
    name = "demo-web"
    image = docker_image.web.image_id
    ports{
        internal = 80
        external = 8080
    }
}