output "cloudfront_url" {
  description = "Public HTTPS URL for the ShowStats app"
  value       = "https://${aws_cloudfront_distribution.app.domain_name}"
}

output "ecr_repository_url" {
  description = "ECR repository URL for pushing Docker images"
  value       = aws_ecr_repository.showstats.repository_url
}

output "public_subnet_ids" {
  description = "Public subnet IDs (used when manually triggering the pipeline task)"
  value       = aws_subnet.public[*].id
}

output "alb_dns_name" {
  description = "ALB DNS name (direct access, bypasses CloudFront)"
  value       = aws_lb.app.dns_name
}