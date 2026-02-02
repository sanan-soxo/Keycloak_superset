resource "keycloak_realm" "superset" {
  realm   = var.realm_name
  enabled = true
}
