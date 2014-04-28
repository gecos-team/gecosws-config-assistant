#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: scripts_launch
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin

    template "/etc/init.d/scripts-launcher" do
      source "scripts_launcher.erb"
      mode "0755"
      owner "root" 
      variables({ :startup => new_resource.on_startup,:shutdown => new_resource.on_shutdown})
      action :create
    end

    service "scripts-launcher" do
      supports :start => true, :stop => true
      action :nothing
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


