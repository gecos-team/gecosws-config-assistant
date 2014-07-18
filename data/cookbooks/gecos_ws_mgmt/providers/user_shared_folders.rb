#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: user_shared_folders
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    pattern = '(smb|nfs|ftp)(:\/\/)([\S]*\/.*)'
    users = new_resource.users
    users.each_key do |user_key|
      username = user_key
      user = users[user_key]
   
      homedir = `eval echo ~#{username}`.gsub("\n","")
      gtkbookmark_files =  ["#{homedir}/.config/gtk-3.0/bookmarks", "#{homedir}/.gtk-bookmarks"]
      gtkbookmark_files.each do |gtkbook|
        if ::File.exists? gtkbook
          clean_file = Chef::Util::FileEdit.new gtkbook
          clean_file.search_file_delete_line(pattern)
          clean_file.write_file
        else
          file gtkbook do
            owner username
            group username
            action :nothing
          end.run_action(:create)
        end
      

        user.gtkbookmarks.each do |bookmark|
          if bookmark.uri.match(pattern)
            line_to_add = "#{bookmark.uri} #{bookmark.uri}"
            
            Chef::Log.info("Agregando accesos directos a carpetas compartidas")
            ::File.open(gtkbook, 'a') do |file|
              file.puts line_to_add
            end
          end

        end
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
    Chef::Log.error(e.message)
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  ensure
    gecos_ws_mgmt_jobids "users_mgmt" do
      provider "gecos_ws_mgmt_jobids"
      resource "user_shared_folders_res"
    end.run_action(:reset)
  end
end
