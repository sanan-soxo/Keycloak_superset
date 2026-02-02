output "superset_client_id" {
  value = keycloak_openid_client.superset.client_id
}

output "superset_client_secret" {
  value     = random_password.superset_secret.result
  sensitive = true
}

output "realm" {
  value = keycloak_realm.superset.realm
}
