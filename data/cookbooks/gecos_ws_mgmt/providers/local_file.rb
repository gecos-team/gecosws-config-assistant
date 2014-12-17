#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: local_file
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
      if new_resource.delete_files.any?
        new_resource.delete_files.each do |value|
        makebackup = 1 if value.backup 
         if ::File.exists?(value.file)
           if ::File.file?(value.file)
             file value.file do
               backup makebackup
               action :nothing
             end.run_action(:delete)
           elsif ::File.directory?(value.file)
             directory value.file do
               recursive true
               action :nothing
             end.run_action(:delete)
           end
         end
        end
      end

      if new_resource.copy_files.any?
        new_resource.copy_files.each do |file|       
          if file.overwrite 
             grp_members = ::Etc.getgrnam(file.group).mem
             remote_file file.file_dest do
               source file.file_orig
               owner file.user
               mode file.mode
               group file.group
               action :nothing
             end.run_action(:create)
           else
             grp_members = ::Etc.getgrnam(file.group).mem 
             remote_file file.file_dest do
                source file.file_orig
                owner file.user
                mode file.mode
                group file.group
                action :nothing
             end.run_action(:create_if_missing)
          end
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
    gecos_ws_mgmt_jobids "local_file_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "misc_mgmt"
    end.run_action(:reset)
  end
end

