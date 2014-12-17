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
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)
      package 'sssd' do
        action :nothing
      end.run_action(:install)

      if new_resource.enabled
        domain = new_resource.domain
        Chef::Log.info("SSSD enabled")
        if domain.type == "ad"
          if ! (new_resource.methods.include?('smb_url') and new_resource.methods.include?('krb5_url') and new_resource.methods.include?('sssd_url'))
            %w(workgroup name).each do |attrib|
              raise "Falta atributo " + attrib unless domain.key?(attrib)
            end
          end
        elsif domain.type == "ldap"
          if ! new_resource.methods.include?('sssd_url')
            %w(name ldap_uri search_base).each do |attrib|
              raise "Falta atributo " + attrib unless domain.key?(attrib)
            end 
          end
        else
          raise "No se ha especificado el tipo de dominio"
        end
        
        if domain.type == "ad"
          if ! (domain.key?('ad_user') and domain.key?('ad_passwd'))
            Chef::Log.info("SSSD_setup: Error to register computer. Administrator credentials incorrects")
            netjoin_command = "net ads info"
          else
            netjoin_command = "net ads join -U #{domain.ad_user}%#{domain.ad_passwd}"
          end

          execute "net-join-ads" do
            command netjoin_command
            action :nothing
            only_if { domain.key?('ad_user') and domain.key?('ad_passwd') }
          end
          res = [['smb_url','/etc/samba/smb.conf','smb.conf.erb'],
                 ['krb5_url','/etc/krb5.conf','krb5.conf.erb']]
          res.each do |url,dst,src|
            if new_resource.methods.include?(url) and !new_resource[url].nil?
              remote_file dst do
                source new_resource[url]
                owner 'root'
                group 'root'
                mode 00644
                notifies :run, "execute[net-join-ads]", :delayed
              end
            else
              template dst do
                source src
                owner 'root'
                group 'root'
                mode 00644
                variables ({
                  :domain => domain
                })
                notifies :run, "execute[net-join-ads]", :delayed
              end
            end
          end
        end

        if new_resource.methods.include?('sssd_url') and !new_resource.sssd_url.nil?
          remote_file "/etc/samba/sssd.conf" do
            source new_resource.sssd_url
            owner 'root'
            group 'root'
            mode 00600
            notifies :restart, "service[sssd]", :delayed
          end
        else
          template '/etc/sssd/sssd.conf' do
            source 'sssd.conf.erb'
            owner 'root'
            group 'root'
            mode 00600
            variables ({
              :domain => domain,
              :enabled => new_resource.enabled
            })
            notifies :restart, "service[sssd]", :delayed
          end
        end

        Chef::Log.info("SSSD_setup: Configuring the domain #{domain.name}")

        # Have authconfig enable SSSD in the pam files
        execute 'pam-auth-update' do
          command 'pam-auth-update --package'
          action :nothing
        end

        cookbook_file '/usr/share/pam-configs/my_mkhomedir' do
          source 'my_mkhomedir'
          owner 'root'
          group 'root'
          mode 00644
          notifies :run, 'execute[pam-auth-update]'
        end

        service 'sssd' do
          provider Chef::Provider::Service::Upstart
          supports :status => true, :restart => true, :reload => true
          action [:enable, :start]
        end
        
        template "/etc/gca-sssd.control" do
          source 'gca-sssd.control.erb'
          variables ({:auth_type => domain.type})
        end
      else
        Chef::Log.info("SSSD disabled")
        domain = new_resource.domain
        if not domain.nil?
          if domain.type == "ad"
            if domain.leave
              execute "net-leave-ads" do
                command "net ads leave -U #{domain.ad_user}%#{domain.ad_passwd}"
                action :nothing
                only_if { domain.key?('ad_user') and domain.key?('ad_passwd') }
              end.run_action(:run)
            end
            res = [['/etc/samba/smb.conf','smb.conf.erb'],
                   ['/etc/krb5.conf','krb5.conf.erb']]
            res.each do |dst,src|
              template dst do
                source src
                owner 'root'
                group 'root'
                mode 00644
                variables ({
                  :domain => domain
                })
               
              end
            end
          end
        end
        template '/etc/sssd/sssd.conf' do
          source 'sssd.conf.erb'
          owner 'root'
          group 'root'
          mode 00600
          variables ({
            :domain => {},
            :enabled => new_resource.enabled
          })
          notifies :restart, "service[sssd]", :delayed
        end
        service 'sssd' do
          provider Chef::Provider::Service::Upstart
          supports :status => true, :restart => true, :reload => true
          action [:stop, :disable]
        end
        
        file "/etc/gca-sssd.control" do
          action :delete
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
    raise e
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      if not e.message.frozen?
        node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
      else
        node.set['job_status'][jid]['message'] = e.message
      end
    end
  end
end


