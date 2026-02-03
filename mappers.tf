resource "keycloak_openid_user_property_protocol_mapper" "email" {
  realm_id  = keycloak_realm.superset.id
  client_id = keycloak_openid_client.superset.id
  name      = "email"

  user_property = "email"
  claim_name    = "email"

  add_to_access_token = true
  add_to_id_token     = true
  add_to_userinfo     = true
}

resource "keycloak_openid_user_property_protocol_mapper" "username" {
  realm_id  = keycloak_realm.superset.id
  client_id = keycloak_openid_client.superset.id
  name      = "username"

  user_property = "username"
  claim_name    = "preferred_username"

  add_to_access_token = true
  add_to_id_token     = true
  add_to_userinfo     = true
}


resource "keycloak_generic_protocol_mapper" "realm_roles" {
  realm_id  = keycloak_realm.superset.id
  client_id = keycloak_openid_client.superset.id

  name            = "realm-roles"
  protocol        = "openid-connect"
  protocol_mapper = "oidc-usermodel-realm-role-mapper"

  config = {
    "claim.name"     = "roles"
    "jsonType.label" = "String"
    "multivalued"    = "true"
  }
}
