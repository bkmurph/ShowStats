resource "aws_scheduler_schedule" "pipeline" {
  name        = "showstats-pipeline-biweekly"
  description = "Run the ShowStats pipeline every other Monday at 8 AM ET"

  schedule_expression          = "rate(14 days)"
  schedule_expression_timezone = "America/New_York"

  flexible_time_window {
    mode                      = "FLEXIBLE"
    maximum_window_in_minutes = 60
  }

  target {
    arn      = aws_ecs_cluster.showstats.arn
    role_arn = aws_iam_role.scheduler.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.pipeline.arn
      launch_type         = "FARGATE"

      network_configuration {
        assign_public_ip = true
        subnets          = aws_subnet.public[*].id
        security_groups  = [aws_security_group.pipeline.id]
      }
    }
  }
}