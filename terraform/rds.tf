data "aws_vpc" "default" {
  id = "${var.vpc_id}"
}

data "aws_subnet_ids" "default" {
  vpc_id = "${data.aws_vpc.default.id}"

  tags {
    component = "private"
    env       = "${var.environment}"
  }
}

data "aws_security_groups" "default" {
  filter {
    name  = "vpc-id"
    values = ["${data.aws_vpc.default.id}"]
  }

  filter {
    name = "tag:env"
    values = ["${var.environment}"]
  }

  filter {
    name = "tag:component"
    values = ["vpn","internal"]
  }
}

module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "${var.environment}-${var.service_name}"

  # All available versions:
# http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.VersionMgmt
  engine            = "postgres"
  engine_version    = "10.6"
  instance_class    = "db.m4.large"
  allocated_storage = 30
  storage_encrypted = true

  name     = "ichain"
  username = "${var.rds_admin_user}"
  password = "${var.rds_admin_password}"
  port     = "5432"

  vpc_security_group_ids = ["${data.aws_security_groups.default.ids}"]
  multi_az  = false 

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"
  apply_immediately   = true
  auto_minor_version_upgrade  = false
  copy_tags_to_snapshot = true

  # disable backups to create DB faster
  backup_retention_period = 3
  storage_type  = "gp2"

  option_group_name     = "default:postgres-10"
  parameter_group_name  = "default.postgres10"

  tags = {
    env = "${var.environment}",
  }

  # DB subnet group
  subnet_ids = ["${data.aws_subnet_ids.default.ids}"]

  # Snapshot name upon DB deletion
  final_snapshot_identifier = "${var.environment}-${var.service_name}-config"
}

#resource "null_resource" "db_setup" {
  # runs after database and security group providing external access is created
#  depends_on = ["module.db"]

#    provisioner "local-exec" {
#      command = "../../scripts/seed-airflow-db.sh ${var.rds_admin_user} ${var.rds_admin_password} ${module.db.this_db_instance_address}"
#    }
#}
