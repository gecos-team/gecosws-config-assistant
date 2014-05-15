#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: local_groups
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    groups_list = new_resource.groups_list

	groups_list.each do |item|
		gid = item.group
		uids = item.users

		group "#{gid}" do
		  action :modify
		  members uids
		  append true
		end
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