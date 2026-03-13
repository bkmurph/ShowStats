resource "aws_s3_bucket" "showstats" {
  bucket = var.s3_bucket

  tags = { Name = "showstats" }
}

resource "aws_s3_bucket_versioning" "showstats" {
  bucket = aws_s3_bucket.showstats.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "showstats" {
  bucket = aws_s3_bucket.showstats.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "showstats" {
  bucket = aws_s3_bucket.showstats.id

  rule {
    id     = "expire-old-versions"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}