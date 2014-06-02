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
      action :nothing
    end.run_action(:install)
 
    if new_resource.enabled
      domain = new_resource.domain
        Chef::Log.info("SSSD activado")
      if domain.type == "ad" 
        %w(workgroup name).each do |attrib|
          raise "Falta atributo " + attrib unless domain.key?(attrib)
        end

        Chef::Log.info("SSSD_setup: Configurando el grupo de trabajo #{domain.workgroup}")
        ad_user = domain.ad_user
        ad_passwd =  domain.ad_passwd
        execute "net-join-ads" do
          command "net ads join -U #{ad_user}%#{ad_passwd}"
          action :nothing 
        end

        if new_resource.methods.include?('smb_url') and !new_resource.smb_url.nil?
          remote_file "/etc/samba/smb.conf" do
            source new_resource.smb_url
            owner 'root'
            group 'root'
            mode 00644
            notifies :run, "execute[net-join-ads]", :delayed
          end
        else
          template '/etc/samba/smb.conf' do
            source 'smb.conf.erb'
            owner 'root'
            group 'root'
            mode 00644
            variables ({
              :domain => domain,
              :realm => domain.name.upcase
            })
            notifies :run, "execute[net-join-ads]", :delayed
          end
        end
   
        if new_resource.methods.include?('krb5_url') and !new_resource.krb5_url.nil?
          remote_file "/etc/krb5.conf" do
            source new_resource.krb5_url
            owner 'root'
            group 'root'
            mode 00644
            notifies :run, "execute[net-join-ads]", :delayed
          end
        else
          template '/etc/krb5.conf' do
            source 'krb5.conf.erb'
            owner 'root'
            group 'root'
            mode 00644
            variables ({
              :realm => domain.name.upcase,
              :domain => domain
            })
            notifies :run, "execute[net-join-ads]", :delayed
          end
        end

      elsif domain.type == "ldap"
        %w(name ldap_uri search_base).each do |attrib|
          raise "Falta atributo " + attrib unless domain.key?(attrib)
        end 
      else
        raise "No se ha especificado el tipo de dominio"
      end
        Chef::Log.info("SSSD_setup: Configurando el dominio #{domain.name}")
  
        # Have authconfig enable SSSD in the pam files
        execute 'pam-auth-update' do
          command 'pam-auth-update --package'
          action :nothing
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
              :domain => domain
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
  
        s = service 'sssd' do
          supports :status => true, :restart => true, :reload => true
          action :nothing
        end
        s.run_action(:enable)
        s.run_action(:start)
        file "/etc/gca-sssd.control" do
            action :create
        end
    else
      Chef::Log.info("SSSD desactivado")
      s = service 'sssd' do
        supports :status => true, :restart => true, :reload => true
        action :nothing
      end
      s.run_action(:disable)
      s.run_action(:stop)
      file "/etc/gca-sssd.control" do
        action :delete
      end
    end

    # save current job ids (new_resource.job_ids) as "ok"
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end

  rescue Exception => e
    raise e.message
    # just save current job ids as "failed"
    # save_failed_job_ids
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end


