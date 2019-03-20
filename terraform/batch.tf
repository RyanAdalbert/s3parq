module "batch" {
  source          = "git::https://github.integrichain.net/sre/tf-batch.git//modules"
  vpc_id            = "${var.vpc_id}"
  service_name      = "${var.service_name}"
  environment       = "${var.environment}"
  instance_type     = ["r5.xlarge"]
  subnet_tag        = "private"
  instance_profile  = "${local.instance_profile}"

  min_vcpus       = 0
  max_vcpus       = 4
}
