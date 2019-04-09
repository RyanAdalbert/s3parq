#----- ECS --------
module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  name    = "${local.resource_service_name}"
}

data "aws_iam_instance_profile" "this" {
  name = "dev_ecs_instance_role"
}

#----- ECS  Resources--------

data "aws_ami" "ichain_ecs" {
  most_recent = true
  owners      = ["687531504312"]

  filter {
    name   = "tag:component"
    values = ["ecs"]
  }
}

data "aws_vpc" "this" {
  id = "${var.vpc_id}"
}

# ----- Subnet -----
data "aws_subnet_ids" "this" {
  vpc_id = "${data.aws_vpc.this.id}"

  tags {
    component = "private"
    env       = "${var.environment}"
  }
}

#----- Security group -----
data "aws_security_groups" "this" {
  filter {
    name    = "vpc-id"
    values  = ["${data.aws_vpc.this.id}"]
  }

  filter {
    name    = "tag:env"
    values  = ["${var.environment}"]
  }

  filter {
    name    = "tag:component"
    values  = ["vpn","internal"]
  }
}

module "this" {
  source = "terraform-aws-modules/autoscaling/aws"

  name = "${local.resource_service_name}"

  # Launch configuration
  lc_name = "${local.resource_service_name}"

  image_id                      = "${data.aws_ami.ichain_ecs.id}"
  instance_type                 = "m5.large"
  security_groups               = ["${data.aws_security_groups.this.ids}"]
  iam_instance_profile          = "${data.aws_iam_instance_profile.this.arn}"
  user_data                     = "${data.template_file.user_data.rendered}"
  target_group_arns             = ["${module.alb.target_group_arns}"]
  recreate_asg_when_lc_changes  = true

  # Auto scaling group
  asg_name                  = "${local.resource_service_name}"
  vpc_zone_identifier       = ["${data.aws_subnet_ids.this.ids}"]
  health_check_type         = "EC2"
  min_size                  = 0
  max_size                  = 2 
  desired_capacity          = 1
  wait_for_capacity_timeout = 0

  tags = [
    {
      key                 = "env"
      value               = "${var.environment}"
      propagate_at_launch = true
    },
    {
      key                 = "cluster"
      value               = "${local.resource_service_name}"
      propagate_at_launch = true
    },
  ]
}

data "template_file" "user_data" {
  template = "${file("${path.module}/templates/user-data.sh")}"

  vars {
    cluster_name = "${local.resource_service_name}"
  }
}

module "alb" {
  source                    = "terraform-aws-modules/alb/aws"
  load_balancer_is_internal = true
  logging_enabled           = false
  log_bucket_name           = "ichain-sam-test"
  log_location_prefix       = "terraform"
  load_balancer_name        = "${local.resource_service_name}"

  security_groups           = ["${data.aws_security_groups.this.ids}"]
  subnets                   = ["${data.aws_subnet_ids.this.ids}"]
  tags                      = "${local.tags}"
  vpc_id                    = "${data.aws_vpc.this.id}"
  http_tcp_listeners        = "${local.http_tcp_listeners}"
  http_tcp_listeners_count  = "${local.http_tcp_listeners_count}"
  target_groups             = "${local.target_groups}"
  target_groups_count       = "${local.target_groups_count}"
}
