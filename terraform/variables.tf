variable "vpc_id"   { default = "" }
variable "environment" { default = "" }
variable "route53_internal_zone_id" { default = "" }
variable "key_name" { default = "" }
variable "iam_instance_profile" { default = "" }

variable "rds_admin_user" { default = "sqladmin" }
variable "rds_admin_password" { default = "cj5ScvdAtz" }
