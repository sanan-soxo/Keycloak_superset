variable "keycloak_url" {
  description = "Keycloak base URL"
  default     = "http://localhost:9090"
}

variable "keycloak_admin_user" {}
variable "keycloak_admin_password" {}

variable "realm_name" {
  default = "superset"
}

variable "superset_base_url" {
  default = "http://localhost:8088"
}
