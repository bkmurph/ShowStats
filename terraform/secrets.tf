resource "aws_secretsmanager_secret" "setlist_fm_api_key" {
  name        = "showstats/setlist-fm-api-key"
  description = "Setlist.fm API key for the ShowStats pipeline"

  tags = { Name = "showstats-setlist-fm-api-key" }
}

resource "aws_secretsmanager_secret_version" "setlist_fm_api_key_placeholder" {
  secret_id     = aws_secretsmanager_secret.setlist_fm_api_key.id
  secret_string = jsonencode({ SETLIST_FM_API_KEY = "REPLACE_ME" })

  lifecycle {
    # Prevent Terraform from overwriting the real key after initial creation
    ignore_changes = [secret_string]
  }
}