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
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "showstats_public_assets" {
  bucket     = aws_s3_bucket.showstats.id
  depends_on = [aws_s3_bucket_public_access_block.showstats]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowPublicReadAssets"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource = [
          "arn:aws:s3:::${var.s3_bucket}/assets/*",
          "arn:aws:s3:::${var.s3_bucket}/2023-05-27+14.55.37.gif",
        ]
      }
    ]
  })
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