#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: file_browser
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)
      users = new_resource.users
      users.each_key do |user_key|
        username = user_key 
        username.gsub!('###','.')
        user = users[user_key]
      
        #default_folder_viewer
        if !user.default_folder_viewer.empty? and !user.default_folder_viewer.nil?
          gecos_ws_mgmt_desktop_setting "default-folder-viewer" do
            value user.default_folder_viewer
            schema "org.nemo.preferences"
            username username
            provider "gecos_ws_mgmt_gsettings"
            action :nothing
          end.run_action(:set)
        end

        #show_hidden_files
        if !user.show_hidden_files.empty? and !user.show_hidden_files.nil? 
          gecos_ws_mgmt_desktop_setting "show-hidden-files" do
            value user.show_hidden_files
            schema "org.nemo.preferences"
            username username
            provider "gecos_ws_mgmt_gsettings"
            action :nothing
          end.run_action(:set)
        end
     
        #show_search_icon_toolbar
        if !user.show_search_icon_toolbar.empty? and !user.show_search_icon_toolbar.nil? 
          gecos_ws_mgmt_desktop_setting "show-search-icon-toolbar" do
            value user.show_search_icon_toolbar
            schema "org.nemo.preferences"
            username username
            provider "gecos_ws_mgmt_gsettings"
            action :nothing
          end.run_action(:set)
        end

        #click_policy
        if !user.click_policy.empty? and !user.click_policy.nil? 
          gecos_ws_mgmt_desktop_setting "click-policy" do
            value user.click_policy
            schema "org.nemo.preferences"
            username username
            provider "gecos_ws_mgmt_gsettings"
            action :nothing
          end.run_action(:set)
        end

        #confirm_trash
        if !user.confirm_trash.empty? and !user.confirm_trash.nil? 
          gecos_ws_mgmt_desktop_setting "confirm-trash" do
            value user.confirm_trash
            schema "org.nemo.preferences"
            username username
            provider "gecos_ws_mgmt_gsettings"
            action :nothing
          end.run_action(:set)
        end


      end
    else
      Chef::Log.info("This resource is not support into your OS")
    end

    # save current job ids (new_resource.job_ids) as "ok"
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end

  rescue Exception => e
    # just save current job ids as "failed"
    # save_failed_job_ids
    Chef::Log.error(e.message)
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      if not e.message.frozen?
        node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
      else
        node.set['job_status'][jid]['message'] = e.message
      end
    end
  ensure
    gecos_ws_mgmt_jobids "file_browser_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end
