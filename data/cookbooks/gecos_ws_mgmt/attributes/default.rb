
default[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:support_os] = ["GECOS V2"]
default[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:network_mgmt][:network_res][:job_ids] = []
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:connections] = []
default[:gecos_ws_mgmt][:network_mgmt][:network_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:auth_type] = ''
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled] = false
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:job_ids] = []
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:updated_by] = {}
default[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:support_os] = ["GECOS V2"]


default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:repo_list] = []
default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:job_ids] = []
default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:updated_by] = {}
default[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:software_mgmt][:package_res][:package_list] = []
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:pkgs_to_remove] = [] 
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:job_ids] = []
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:updated_by] = {}
default[:gecos_ws_mgmt][:software_mgmt][:package_res][:support_os] = ["GECOS V2", "Ubuntu 14.04.1 LTS"]

default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:citrix_config] = {}  
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:java_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:firefox_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:loffice_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:thunderbird_config] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:job_ids] = [] 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:updated_by] = {} 
default[:gecos_ws_mgmt][:software_mgmt][:app_config_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:printers_list] = []
default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:job_ids] = []
default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:updated_by] = {}
default[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:onstop_update] = false
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:onstart_update] = false
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:days] = []
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:date] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:server] = ""
default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:cpu_freq_gov] = ""
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:auto_shutdown] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:usb_autosuspend] = ""
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:users_list] =[]
default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:job_ids] =[]
default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:delete_files] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:copy_files] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_startup] = []
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_shutdown] = []
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:groups_list] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:local_admin_list] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:job_ids] = []
default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:updated_by] = {}
default[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:support_os] = []

default[:gecos_ws_mgmt][:users_mgmt][:desktop_control_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:desktop_control_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:desktop_control_res][:support_os] = []

default[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:support_os] = ["GECOS V2"]

default[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:support_os] = []

default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:users] = {}
default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:systemset] = false
default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:systemlock] = false
default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:job_ids] = []
default[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:support_os] = ["GECOS V2"]

