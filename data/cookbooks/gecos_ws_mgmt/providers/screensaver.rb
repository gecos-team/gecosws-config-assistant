#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: screensaver
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do

  begin
  #  users = node[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:users] #if new_resource.users.nil?
    users = new_resource.users
    users.each do |user|
      username = user.username
      idle_enabled = user.idle_enabled
      idle_delay = user.idle_delay
      lock_enabled = user.lock_enabled
      lock_delay = user.lock_delay
### TO-DO:
## Sacar el tipo de sesion con el plugin de ohai x-session-manager.rb (amunoz)
## Distinguir entre sesion Cinnamon y LXDE

#     session = node["desktop_session"] 
      gecos_ws_mgmt_desktop_setting "idle-activation-enabled" do
        type "string"
        value idle_enabled
        schema "org.cinnamon.desktop.screensaver"
        username user.username
        provider "gecos_ws_mgmt_gsettings"
        action :set
      end
  
      gecos_ws_mgmt_desktop_setting "lock-enabled" do
        type "string"
        value lock_enabled
        schema "org.cinnamon.desktop.screensaver"
        username user.username
        provider "gecos_ws_mgmt_gsettings"
        action :set
      end
  
      gecos_ws_mgmt_desktop_setting "idle-delay" do
        type "string"
        value idle_delay
        schema "org.cinnamon.desktop.session"
        username user.username
        provider "gecos_ws_mgmt_gsettings"
        action :set
      end
  
      gecos_ws_mgmt_desktop_setting "lock-delay" do
        type "string"
        value lock_delay
        schema "org.cinnamon.desktop.screensaver"
        username user.username
        provider "gecos_ws_mgmt_gsettings"
        action :set
      end
    end
    rescue
      # TODO:
      # just save current job ids as "failed"
      # save_failed_job_ids
      raise
    end
end

