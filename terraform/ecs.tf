resource "aws_ecs_cluster" "showstats" {
  name = "showstats"

  tags = { Name = "showstats" }
}

# --- App Task Definition ---
resource "aws_ecs_task_definition" "app" {
  family                   = "showstats-app"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([{
    name      = "showstats-app"
    image     = "${aws_ecr_repository.showstats.repository_url}:${var.app_image_tag}"
    essential = true

    portMappings = [{
      containerPort = 8050
      protocol      = "tcp"
    }]

    healthCheck = {
      command     = ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:8050/health')\" || exit 1"]
      interval    = 30
      timeout     = 10
      retries     = 3
      startPeriod = 120
    }

    environment = [
      { name = "SHOWSTATS_S3_BUCKET", value = var.s3_bucket },
      { name = "AWS_DEFAULT_REGION", value = var.aws_region },
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.app.name
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

# --- App Service ---
resource "aws_ecs_service" "app" {
  name            = "showstats-app"
  cluster         = aws_ecs_cluster.showstats.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  health_check_grace_period_seconds = 120

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "showstats-app"
    container_port   = 8050
  }

  depends_on = [aws_lb_listener.http]
}

# --- Pipeline Task Definition (no service — run on schedule) ---
resource "aws_ecs_task_definition" "pipeline" {
  family                   = "showstats-pipeline"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.pipeline_task.arn

  container_definitions = jsonencode([{
    name      = "showstats-pipeline"
    image     = "${aws_ecr_repository.showstats.repository_url}:${var.app_image_tag}"
    essential = true

    command = [
      "/app/.venv/bin/python", "-m", "showstats.pipeline.build_dataset"
    ]

    environment = [
      { name = "SHOWSTATS_S3_BUCKET", value = var.s3_bucket },
      { name = "AWS_DEFAULT_REGION", value = var.aws_region },
    ]

    secrets = [{
      name      = "SETLIST_FM_API_KEY"
      valueFrom = "${aws_secretsmanager_secret.setlist_fm_api_key.arn}:SETLIST_FM_API_KEY::"
    }]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.pipeline.name
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}