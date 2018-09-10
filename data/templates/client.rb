# Configuration File For Chef (chef-client)
#

log_level           :info

log_location        STDOUT

ssl_verify_mode    ${ssl_certificate_verification}

chef_server_url     "${chef_url}"

file_cache_path     "/var/cache/chef"

file_backup_path    "/var/lib/chef/backup"

pid_file            "/var/run/chef/client.pid"

require "/usr/share/gecosws-config-assistant/report-handlers/gecoshandlers"
reporthandler = GECOSReports::StatusHandler.new
report_handlers << reporthandler
exception_handlers << reporthandler

cache_options({ :path => "/var/cache/chef/checksums", :skip_expires => true})

#{IF ohai_new_config_syntax}
ohai.disabled_plugins = ['applications','c','erlang','groovy','java','lua','network_listeners','php','ip_scopes','passwd']
#{ENDIF}

#{IF ohai_old_config_syntax}
Ohai::Config[:disabled_plugins] = ['applications','c','erlang','groovy','java','lua','network_listeners','php','ip_scopes','passwd']
#{ENDIF}

node_name           "${chef_node_name}"

client_key          "/etc/chef/client.pem"
