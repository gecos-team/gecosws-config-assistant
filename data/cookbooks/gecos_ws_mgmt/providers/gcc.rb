#
# Cookbook Name:: gecos_ws_mgmt
# Recipe:: gcc
#
# Copyright 2013, Limelight Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
require 'json'

action :setup do
  begin
    gem_depends = [ 'rest_client' ]

    gem_depends.each do |gem|
      gem_package gem do
        gem_binary("/opt/chef/embedded/bin/gem")
        action :nothing
      end.run_action(:install)
    end

    Gem.clear_paths
    require 'rest_client'
    if new_resource.run_attr
      if new_resource.gcc_link
        if not new_resource.uri_gcc.nil? and not new_resource.gcc_nodename.nil? and not new_resource.gcc_username.nil? and not new_resource.gcc_pwd_user.nil? and not new_resource.gcc_selected_ou.nil?
          Chef::Log.info("GCC: Configurndo GECOS Control Center")
          begin
            resource = RestClient::Resource.new(new_resource.uri_gcc + '/register/computer/', :user => new_resource.gcc_username, :password => new_resource.gcc_pwd_user)
            response = resource.post :node_id => new_resource.gcc_nodename,:ou_name=>new_resource.gcc_selected_ou, :content_type => :json, :accept => :json
            if not response.code.between?(200,299)
              Chef::Log.error('The GCC URI not response')  
            else
              response_json = JSON.load(response.to_str)
              if not response_json['ok']
                Chef::Log.error(response_json['message'])
              end
            end
          rescue Exception => e
            Chef::Log.error(e.message)
          end
          template "/etc/gcc.control" do
            source 'gcc.control.erb'
            owner "root"
            group "root"
            mode 00755
            variables({
              :uri_gcc => new_resource.uri_gcc,
              :gcc_username => new_resource.gcc_username, 
              :gcc_nodename => new_resource.gcc_nodename
            })
          end 
        end
      else
        if not new_resource.uri_gcc.nil? and not new_resource.gcc_nodename.nil? and not new_resource.gcc_username.nil? and not new_resource.gcc_pwd_user.nil? and not new_resource.gcc_selected_ou.nil?
          Chef::Log.info("GCC: Desenlazando cliente de GECOS Control Center")
          begin
            resource = RestClient::Resource.new(new_resource.uri_gcc + '/register/computer/?node_id=' + new_resource.gcc_nodename, :user => new_resource.gcc_username, :password => new_resource.gcc_pwd_user)
            response = resource.delete
            if not response.code.between?(200,299)
              Chef::Log.error('The GCC URI not response')  
            else
              response_json = JSON.load(response.to_str)
              if not response_json['ok']
                Chef::Log.error(response_json['message'])
              end
            end
          rescue Exception => e
            Chef::Log.error(e.message)
          end
          file "/etc/gcc.control" do
            action :nothing
          end.run_action(:delete)
        end
      end
    else
      template "/etc/gcc.control" do
        source 'gcc.control.erb'
        owner "root"
        group "root"
        mode 00755
        variables({
          :uri_gcc => new_resource.uri_gcc,
          :gcc_username => new_resource.gcc_username, 
          :gcc_nodename => new_resource.gcc_nodename
        })
      end
      Chef::Log.info('Not running')
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
    raise e.message
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end


