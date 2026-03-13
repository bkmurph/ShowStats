variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket" {
  description = "S3 bucket name for showstats data"
  type        = string
  default     = "showstats1"
}

variable "app_image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "scheduler_start_date" {
  description = "ISO 8601 start date for the bi-weekly pipeline schedule (set to the first target Monday at 13:00 UTC / 8 AM ET after deployment)"
  type        = string
  default     = "2026-03-16T13:00:00Z"
}