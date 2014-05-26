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

    users = new_resource.users
    
    users.each do |usr|


      #default_folder_viewer
      if !usr.default_folder_viewer.empty? and !usr.default_folder_viewer.nil?
        gecos_ws_mgmt_desktop_setting "default-folder-viewer" do
          value usr.default_folder_viewer
          schema "org.nemo.preferences"
          username usr.username
          provider "gecos_ws_mgmt_gsettings"
          action :nothing
        end.run_action(:set)
      end

      #show_hidden_files
      if !usr.show_hidden_files.empty? and !usr.show_hidden_files.nil? 
        gecos_ws_mgmt_desktop_setting "show-hidden-files" do
          value usr.show_hidden_files
          schema "org.nemo.preferences"
          username usr.username
          provider "gecos_ws_mgmt_gsettings"
          action :nothing
        end.run_action(:set)
      end
   
      #show_search_icon_toolbar
      if !usr.show_search_icon_toolbar.empty? and !usr.show_search_icon_toolbar.nil? 
        gecos_ws_mgmt_desktop_setting "show-search-icon-toolbar" do
          value usr.show_search_icon_toolbar
          schema "org.nemo.preferences"
          username usr.username
          provider "gecos_ws_mgmt_gsettings"
          action :nothing
        end.run_action(:set)
      end

      #click_policy
      if !usr.click_policy.empty? and !usr.click_policy.nil? 
        gecos_ws_mgmt_desktop_setting "click-policy" do
          value usr.click_policy
          schema "org.nemo.preferences"
          username usr.username
          provider "gecos_ws_mgmt_gsettings"
          action :nothing
        end.run_action(:set)
      end

      #confirm_trash
      if !usr.confirm_trash.empty? and !usr.confirm_trash.nil? 
        gecos_ws_mgmt_desktop_setting "confirm-trash" do
          value usr.confirm_trash
          schema "org.nemo.preferences"
          username usr.username
          provider "gecos_ws_mgmt_gsettings"
          action :nothing
        end.run_action(:set)
      end


    end

    # save current job ids (new_resource.job_ids) as "ok"
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end

  rescue Exception => e
    # just save current job ids as "failed"
    # save_failed_job_ids
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end