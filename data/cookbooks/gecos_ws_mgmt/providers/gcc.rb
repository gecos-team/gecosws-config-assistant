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

      r = gem_package gem do
        action :nothing
      end
      r.run_action(:install)

    end
    Gem.clear_paths
    require 'rest_client'
    if new_resource.gcc_link
      if not new_resource.uri_gcc.nil? and not new_resource.gcc_nodename.nil? and not new_resource.gcc_username.nil? and not new_resource.gcc_pwd_user.nil? and not new_resource.gcc_selected_ou.nil?
        Chef::Log.info("GCC: Configurndo GECOS Control Center")
        resource = RestClient::Resource.new(new_resource.uri_gcc + '/register/computer/', :user => new_resource.gcc_username, :password => new_resource.gcc_pwd_user)
        response = resource.post :node_id => new_resource.gcc_nodename,:ou_name=>new_resource.gcc_selected_ou, :content_type => :json, :accept => :json
        if not response.code.between?(200,299)
          raise 'The GCC URI not response'  
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
        resource = RestClient::Resource.new(new_resource.uri_gcc + '/register/computer/', :user => new_resource.gcc_username, :password => new_resource.gcc_pwd_user)
        response = resource.delete :node_id => new_resource.gcc_nodename, :content_type => :json, :accept => :json
        if not response.code.between?(200,299)
          raise 'The GCC URI not response' 
        end
        file "/etc/gcc.control" do
          action :delete
        end
      end
    end

    #@chefapi = ChefApi::API.new({server:'https://192.168.13.224', client_name: 'test', key_file: '/etc/chef/validation.pem'})
    #puts @chefapi.get_request('/nodes')      
    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"
  rescue
  # TODO:
  # just save current job ids as "failed"
  # save_failed_job_ids
    raise
  end
end


