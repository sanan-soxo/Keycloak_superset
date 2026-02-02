resource "keycloak_role" "admin" {
  realm_id = keycloak_realm.superset.id
  name     = "KeycloakAdmin"
}

resource "keycloak_role" "alpha" {
  realm_id = keycloak_realm.superset.id
  name     = "KeycloakAlpha"
}

resource "keycloak_role" "gamma" {
  realm_id = keycloak_realm.superset.id
  name     = "KeycloakGamma"
}
