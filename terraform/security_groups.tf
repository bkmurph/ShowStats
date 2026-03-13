resource "aws_security_group" "alb" {
  name        = "showstats-alb"
  description = "Allow HTTP from internet (CloudFront fronts this)"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "showstats-alb" }
}

resource "aws_security_group" "app" {
  name        = "showstats-app"
  description = "Allow traffic from ALB only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8050
    to_port         = 8050
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "showstats-app" }
}

resource "aws_security_group" "pipeline" {
  name        = "showstats-pipeline"
  description = "Outbound only - pipeline fetches from external APIs and writes to S3"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "showstats-pipeline" }
}