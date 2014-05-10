#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: local_admin_users
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    local_admin_list = new_resource.local_admin_list

	group "sudo" do
	  action :modify
	  members local_admin_list
	  append true
	end

    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"
    # raise errors when both username/group not exists

  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end