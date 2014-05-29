default[:gecos_ws_mgmt][:network_mgmt][:network_res][:ip_address] = ''
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:gateway] = ''
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:netmask] = ''
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:dns_servers] = []
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:network_type] = 'wired'
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:use_dhcp] = true
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:users] = []
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:job_ids] = []
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:updated_by] = []

default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:domain_list] = []
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:workgroup] = ''
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled] = false
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:job_ids] = []
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:updated_by] = []

default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:repo_list] = []
default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:job_ids] = []
default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:updated_by] = []

default[:gecos_ws_mgmt][:software_mgmt][:package_res][:package_list] = []
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:pkgs_to_remove] = [] 
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:job_ids] = []
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:updated_by] = []

default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:adobe_config] = {}  
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:java_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:firefox_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:thunderbird_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:job_ids] = [] 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:updated_by] = [] 

default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:printers_list] = []
default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:job_ids] = []
default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:onstop_update] = false
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:onstart_update] = false
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:days] = []
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:date] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:server] = ""
default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:cpu_freq_gov] = ""
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:auto_shutdown] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:usb_autosuspend] = ""
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:users_list] =[]
default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:job_ids] =[]
default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:updated_by] =[]

default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:delete_files] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:copy_files] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_startup] = []
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_shutdown] = []
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:groups_list] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:local_admin_list] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:updated_by] = []

default[:gecos_ws_mgmt][:misc_mgmt][:desktop_background_res][:desktop_file] = ''
default[:gecos_ws_mgmt][:misc_mgmt][:desktop_background_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:desktop_background_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:desktop_control_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_control_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_control_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:folder_sync] = []
default[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:updated_by] = []

default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:users] = []
default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:updated_by] = []

