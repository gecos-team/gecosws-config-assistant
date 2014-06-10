#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: network
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#


action :setup do

  begin
    # setup resource depends
    gem_depends = [ 'netaddr' ]

    gem_depends.each do |gem|
      gem_package gem do
        gem_binary("/opt/chef/embedded/bin/gem")
        action :nothing
      end.run_action(:install)
    end

    Gem.clear_paths
    require 'netaddr'
    require 'fileutils'

    # setup system connections
    ip_address = new_resource.ip_address
    gateway = new_resource.gateway
    netmask = new_resource.netmask
    network_type = new_resource.network_type
    use_dhcp = new_resource.use_dhcp
    dns_servers_array = new_resource.dns_servers_array

    users = new_resource.users

    nm_conn_backup_dir = '/etc/NetworkManager/system-connections/chef-backups'
    nm_conn_production_dir = '/etc/NetworkManager/system-connections/chef-conns'
 
    unless Kernel::test('d', nm_conn_backup_dir)
      FileUtils.mkdir nm_conn_backup_dir
    end
    
    unless Kernel::test('d', nm_conn_production_dir)
      FileUtils.mkdir nm_conn_production_dir
    end
        
    nm_wired_dhcp_conn_source = 'wired-dhcp-conn.erb'
    nm_wired_static_ip_conn_source = 'wired-static-ip-conn.erb'
    
    nm_macaddress = node["macaddress"].gsub(/[0]([\w]:)/, '\\1')
    
    nm_conn_files = []
    Dir["/etc/NetworkManager/system-connections/*"].each do |conn_file|
      if Kernel::test('f', conn_file)
        unless open(conn_file).grep(/#{node["macaddress"]}/).empty? and open(conn_file).grep(/#{nm_macaddress}/).empty?
          nm_conn_files << conn_file
        end
      end
    end
    
    # parse dns servers
    dns_servers = ""
    dns_servers_array.each do |server|
      if dns_servers.empty?
        dns_servers = server + ";" unless server.empty?
      else
        dns_servers = dns_servers + server + ";" unless server.empty?
      end
    end
    
    if network_type == 'wired'
      if use_dhcp == true
        unless nm_conn_files.empty?
          nm_conn_files.each do |conn_file|
            FileUtils.cp(conn_file, nm_conn_backup_dir)
            basename = ::File.basename(conn_file)
            template_name = nm_conn_production_dir + "/" + basename
            template template_name do
              owner "root"
              group "root"
              mode 0600
              variables ( { :mac_address => nm_macaddress } )
              source nm_wired_dhcp_conn_source
            end
          end
        else
          conn_file = "/etc/NetworkManager/system-connections/chef-conns/chef-managed-connection"
          template conn_file do
            owner "root"
            group "root"
            mode 0600
            variables ( { :mac_address => nm_macaddress } )
            source nm_wired_dhcp_conn_source
          end
        end
      else
        netmask_int = NetAddr.netmask_to_i(netmask)
        netmask = NetAddr.i_to_bits(netmask_int)
        unless nm_conn_files.empty?
          nm_conn_files.each do |conn_file|
            FileUtils.cp(conn_file,nm_conn_backup_dir)
            basename = ::File.basename(conn_file)
            template_name = nm_conn_production_dir + "/" + basename
            template template_name do
              owner "root"
              group "root"
              mode 0600
              variables ( { :dns_servers => dns_servers,
                            :mac_address => nm_macaddress,
                            :ip_address => ip_address,
                            :netmask => netmask,
                            :gateway => gateway } )
              source nm_wired_static_ip_conn_source
            end
          end
        else
          conn_file = "/etc/NetworkManager/system-connections/chef-conns/chef-managed-connection"
          template conn_file do
            owner "root"
            group "root"
            mode 0600
            variables ( { :dns_servers => dns_servers,
                          :mac_address => nm_macaddress,
                          :ip_address => ip_address,
                          :netmask => netmask,
                          :gateway => gateway })
            source nm_wired_static_ip_conn_source
          end
        end
      end
    # TODO: else: wireless connection
    #else 
    end

    # setup user connections
    users_array.each do |user_conn|
      username = user_conn[:username]
    end

    cookbook_file "/etc/init/gecos-nm.conf" do
      source "gecos-nm.conf" 
      mode "0644"
      backup false
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
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end
