#
# Cookbook Name:: gecos_ws_mgmt
# Recipe:: sssd
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

    package 'sssd' do
      action :install
    end
 
    if new_resource.enabled
      if new_resources.methods.include?('workgroup') and new_resource.workgroup_url.empty?
        Chef::Log.info("SSSD sin configuracion correcta")
      else      
        Chef::Log.info("SSSD activado")
        Chef::Log.info("SSSD_setup: Configurando el grupo de trabajo #{new_resource.workgroup}")
        new_resource.domain_list.each do |domain|
          Chef::Log.info("SSSD_setup: Configurando el dominio #{domain.domain_name}")
        end 
  
        # Have authconfig enable SSSD in the pam files
        execute 'pam-auth-update' do
          command 'pam-auth-update --package'
          action :nothing
        end
   
        if new_resource.methods.include?('smb_url') and !new_resource.smb_url.nil?
          remote_file "/etc/samba/smb.conf" do
            source new_resource.smb_url
            owner 'root'
            group 'root'
            mode 00644
          end
        else
          template '/etc/samba/smb.conf' do
            source 'smb.conf.erb'
            owner 'root'
            group 'root'
            mode 00644
            variables ({
              :workgroup => new_resource.workgroup,
              :realm => new_resource.domain_list[0].domain_name.upcase
            })
          end
        end
   
        if new_resource.methods.include?('krb5_url') and !new_resource.krb5_url.nil?
          remote_file "/etc/krb5.conf" do
            source new_resource.krb5_url
            owner 'root'
            group 'root'
            mode 00644
          end
        else
          template '/etc/krb5.conf' do
            source 'krb5.conf.erb'
            owner 'root'
            group 'root'
            mode 00644
            variables ({
              :realm => new_resource.domain_list[0].domain_name.upcase,
              :domain => new_resource.domain_list
            })
          end
        end
  
        if new_resource.methods.include?('sssd_url') and !new_resource.sssd_url.nil?
          remote_file "/etc/samba/sssd.conf" do
            source new_resource.sssd_url
            owner 'root'
            group 'root'
            mode 00644
          end
        else
          template '/etc/sssd/sssd.conf' do
            source 'sssd.conf.erb'
            owner 'root'
            group 'root'
            mode 00600
            variables ({
              :domain => new_resource.domain_list
            })
          end
        end
  
        cookbook_file '/usr/share/pam-configs/my_mkhomedir' do
          source 'my_mkhomedir'
          owner 'root'
          group 'root'
          mode 00644
          notifies :run, 'execute[pam-auth-update]'
        end
  
        service 'sssd' do
          supports :status => true, :restart => true, :reload => true
          action [:enable, :start]
        end
      end 
    else
      Chef::Log.info("SSSD desactivado")
      service 'sssd' do
        supports :status => true, :restart => true, :reload => true
        action [:disable, :stop]
      end 
    end

  rescue
    raise
  end
end


