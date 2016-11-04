# Configuration File For Chef (chef-client)
#

log_level           :info

log_location        STDOUT

chef_server_url     "${chef_url}"

file_cache_path     "/var/cache/chef"

file_backup_path    "/var/lib/chef/backup"

pid_file            "/var/run/chef/client.pid"

require "/usr/share/gecosws-config-assistant/report-handlers/gecoshandlers"
reporthandler = GECOSReports::StatusHandler.new
report_handlers << reporthandler
exception_handlers << reporthandler

cache_options({ :path => "/var/cache/chef/checksums", :skip_expires => true})
Ohai::Config[:disabled_plugins] =['applications','c','erlang','groovy','java','lua','network_listeners','php','ip_scopes','passwd']

node_name           "${chef_node_name}"

client_key          "/etc/chef/client.pem"
