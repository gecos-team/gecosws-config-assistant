#
# Cookbook Name:: gecos_ws_mgmt
# Recipe:: chef
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

action :setup do
  begin
    package 'chef' do
      action :nothing
    end.run_action(:install)
    if not new_resource.chef_link_existing
      if new_resource.chef_link
        if not new_resource.chef_server_url.nil?
          Chef::Log.info("Chef: Configurndo Chef")
          template '/etc/chef/client.rb' do
            source 'client.rb.erb'
            owner 'root'
            group 'root'
            mode 00644
            variables({
              :chef_url => new_resource.chef_server_url,
              :chef_admin_name => new_resource.chef_admin_name,
              :chef_node_name => new_resource.chef_node_name
            })
          end
          remote_file "Copy validation.pem" do
            path "/etc/chef/validation.pem"
            source "file://" + new_resource.chef_validation_pem
            owner 'root'
            group 'root'
            mode 00644
          end      
          Chef::Log.info("Chef: Enlazando al servidor Chef")
          execute 'chef-client' do
            environment 'LANG' => 'es_ES.UTF-8', 'LC_ALL' => 'es_ES.UTF-8', 'HOME' => ENV['HOME']
            command 'chef-client -j /usr/share/gecosws-config-assistant/base.json'
            action :run
          end
       
          Chef::Log.info("Activando servicio chef-client")
          service 'chef-client' do
            provider Chef::Provider::Service::Upstart
            supports :status => true, :restart => true, :reload => true
            action [:enable, :start]
          end
          Chef::Log.info("Chef: Creando fichero de control")
          template "/etc/chef.control" do
            source 'chef.control.erb'
            owner "root"
            group "root"
            mode 00755
            variables({
              :chef_url => new_resource.chef_server_url,
              :chef_admin_name => new_resource.chef_admin_name,
              :chef_node_name => new_resource.chef_node_name
            })
          end 
          Chef::Log.info("Chef: Enliminando validation.pem")
          file "/etc/chef/validation.pem" do
            action :delete
          end
        end 
      else
        Chef::Log.info("Chef: Configurndo Chef")
        template '/etc/chef/client.rb' do
          source 'client.rb.erb'   
          owner 'root'   
          group 'root'   
          mode 00644
          variables({
            :chef_url => "CHEF_URL",
            :chef_admin_name => "ADMIN_NAME",
            :chef_node_name => "NODE_NAME"
          })
        end
        Chef::Log.info("Chef: Configurndo Knife")
        template '/etc/chef/knife.rb' do
          source 'knife.rb.erb'
          owner 'root'
          group 'root'
          mode 00644
          variables({
            :chef_url => new_resource.chef_server_url,
            :chef_admin_name => new_resource.chef_admin_name
          })
        end
        Chef::Log.info("Borrando nodo " + new_resource.chef_node_name)
        execute 'Knife Delete' do
          command 'knife node delete \'' + new_resource.chef_node_name + '\' -c /etc/chef/knife.rb -y'
          action :run
        end
        Chef::Log.info("Borrando cliente " + new_resource.chef_node_name)
        execute 'Knife Delete' do
          command 'knife client delete \'' + new_resource.chef_node_name + '\' -c /etc/chef/knife.rb -y'
          action :run
        end

        Chef::Log.info("Desactivando servicio chef-client")
        service 'chef-client' do
          provider Chef::Provider::Service::Upstart
          supports :status => true, :restart => true, :reload => true
          action [:disable, :stop]
        end
        
        Chef::Log.info("Chef: Elminando fichero de control")
        file "/etc/chef.control" do
          action :delete
        end
        Chef::Log.info("Chef: Eliminando client.pem")
        file "/etc/chef/client.pem" do
          action :delete
        end
        Chef::Log.info("Chef: Eliminando validation.pem")
        file "/etc/chef/validation.pem" do
          action :delete
        end
        Chef::Log.info("Chef: Eliminando knife.rb")
        file "/etc/chef/knife.rb" do
          action :delete
        end
      end
    else
      Chef::Log.info("Chef: Configurndo Knife")
      template '/etc/chef/knife.rb' do
        source 'knife.rb.erb'
        owner 'root'
        group 'root'
        mode 00644
        variables({
          :chef_url => new_resource.chef_server_url,
          :chef_admin_name => new_resource.chef_admin_name
        })
      end
      Chef::Log.info("Chef: Configurndo Chef")
      template '/etc/chef/client.rb' do
        source 'client.rb.erb'
        owner 'root'
        group 'root'
        mode 00644
        variables({
          :chef_url => new_resource.chef_server_url,
          :chef_admin_name => new_resource.chef_admin_name,
          :chef_node_name => new_resource.chef_node_name
        })
      end
      Chef::Log.info("Chef: Creando fichero de control")
      template "/etc/chef.control" do
        source 'chef.control.erb'
        owner "root"
        group "root"
        mode 00755
        variables({
          :chef_url => new_resource.chef_server_url,
          :chef_admin_name => new_resource.chef_admin_name,
          :chef_node_name => new_resource.chef_node_name
        })
      end
      Chef::Log.info("Reregistrando el cliente " + new_resource.chef_node_name)
      execute 'Knife Reregrister' do
        command 'knife client reregister \'' + new_resource.chef_node_name + '\' -c /etc/chef/knife.rb > /etc/chef/client.pem'
        action :run
      end
      Chef::Log.info("Chef: Enlazando al servidor Chef")
      execute 'chef-client' do
        environment 'LANG' => 'es_ES.UTF-8', 'LC_ALL' => 'es_ES.UTF-8', 'HOME' => ENV['HOME']
        command 'chef-client -j /usr/share/gecosws-config-assistant/base.json'
        action :run
      end
    end
  rescue Exception => e
    Chef::Log.error(e.message)
    raise e.message
  end
end


