locals {

  tags = "${map("env", "${var.environment}",
                "role", "airflow",
  )}"

  # This is the convention we use to know what belongs to each other
  resource_service_name  = "${var.environment}-${var.service_name}"
  instance_profile = "dev_ecs_instance_role"

  http_tcp_listeners_count = 1
  http_tcp_listeners = "${list(
                          map(
                              "port", 80,
                              "protocol", "HTTP",
                          ),
                      )}" 

  target_groups_count = 1

  target_groups = "${list(
                        map("name", "${local.resource_service_name}",
                            "backend_protocol", "HTTP",
                            "backend_port", 80,
                            "health_check_path", "/admin/versionview/",
                            "health_check_matcher", "200,302",
                        )
                   )}"
}
