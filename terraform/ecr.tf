resource "aws_ecr_repository" "showstats" {
  name                 = "showstats"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "showstats" }
}

resource "aws_ecr_lifecycle_policy" "showstats" {
  repository = aws_ecr_repository.showstats.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 5 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 5
      }
      action = { type = "expire" }
    }]
  })
}