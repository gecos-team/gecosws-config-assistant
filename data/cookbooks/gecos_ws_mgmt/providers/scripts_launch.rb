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

  on_startup = new_resource.on_startup
  on_shutdown = new_resource.on_shutdown

  if !on_startup.nil? or !on_startup.empty?
    template "/etc/init.d/scripts-onstartup" do
      source "scripts_onstartup.erb"
      mode "0755"
      owner "root" 
      variables({ :startup => on_startup})
      action :create
    end

    bash "enable on start scripts" do
      code <<-EOH
      update-rc.d scripts-onstartup start 60 2 .
      EOH
    end
  else
    file "/etc/init.d/scripts-onstartup" do
      action :nothing
    end.run_action(:delete)

    link "/etc/rc2.d/S60scripts-onstartup" do
      action :nothing
      only_if "test -L /etc/rc2.d/S60scripts-onstartup"
    end.run_action(:delete)
  end

  if !on_shutdown.nil? or !on_shutdown.empty?
    template "/etc/init.d/scripts-onshutdown" do
      source "scripts_onshutdown.erb"
      mode "0755"
      owner "root" 
      variables({ :shutdown => on_shutdown})
      action :create
    end

    bash "enable on shutdown scripts" do
      code <<-EOH
      update-rc.d scripts-onshutdown stop 15 6 0 .
      EOH
    end
  else
    file "/etc/init.d/scripts-onshutdown" do
      action :nothing
    end.run_action(:delete)

    link "/etc/rc6.d/S20scripts-onshutdown" do
      action :nothing
      only_if "test -L /etc/rc6.d/S20scripts-onshutdown"
    end.run_action(:delete)
  end


  job_ids = new_resource.job_ids
  job_ids.each do |jid|
    node.set['job_status'][jid]['status'] = 0
  end

  rescue Exception => e
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
    
  end
end


