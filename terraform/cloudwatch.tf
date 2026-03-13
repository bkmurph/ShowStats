resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/showstats-app"
  retention_in_days = 30

  tags = { Name = "showstats-app" }
}

resource "aws_cloudwatch_log_group" "pipeline" {
  name              = "/ecs/showstats-pipeline"
  retention_in_days = 90

  tags = { Name = "showstats-pipeline" }
}