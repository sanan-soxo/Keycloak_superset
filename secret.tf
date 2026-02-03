resource "random_password" "superset_secret" {
  length  = 32
  special = false
}
