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
    new_resource.users.each do |user|
   
      homedir = `eval echo ~#{user.username}`.gsub("\n","")
      gtkbookmark_file =  "#{homedir}/.gtk-bookmarks"

      if ::File.exists? gtkbookmark_file
        clean_file = Chef::Util::FileEdit.new gtkbookmark_file
        clean_file.search_file_delete_line(pattern)
        clean_file.write_file
      else
        file gtkbookmark_file do
          owner user.username
          group user.username
          action :create
        end
      end

      user.gtkbookmarks.each do |bookmark|
        if bookmark.uri.match(pattern)
          line_to_add = "#{bookmark.uri} #{bookmark.title}"
          
          Chef::Log.info("Agregando accesos directos a carpetas compartidas")         
          add_to_file = Chef::Util::FileEdit.new gtkbookmark_file
          add_to_file.insert_line_if_no_match(pattern, line_to_add)
          add_to_file.write_file
        end

      end
   end

    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"

  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end

