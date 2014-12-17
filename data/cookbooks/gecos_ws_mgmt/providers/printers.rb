#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: printers
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    printers_list = new_resource.printers_list

    if printers_list.any?

      service "cups" do
        action :nothing
      end.run_action(:restart)
      pkgs = ['python-cups', 'cups-driver-gutenprint', 'foomatic-db', 'foomatic-db-engine', 'foomatic-db-gutenprint', 'smbclient']
      pkgs.each do |pkg|
        package pkg do
          action :nothing
        end.run_action(:install)
      end
      
 
      printers_list.each do |printer|
        Chef::Log.info("Installing printer #{printer.name}")
  
        name = printer.name
        make = printer.manufacturer
        model = printer.model
        oppolicy = 'default'
        if printer.attribute?("oppolicy")
          oppolicy = printer.oppolicy
        end
        ppd = ""
        if printer.attribute?("ppd")
          ppd = printer.ppd
        end

        uri = printer.uri
        ppd_uri = ""
        if printer.attribute?("ppd_uri")
          ppd_uri = printer.ppd_uri
        end


        if ppd_uri != '' and ppd != ''
          FileUtils.mkdir_p("/usr/share/ppd/#{make}/#{model}")    
          remote_file "/usr/share/ppd/#{make}/#{model}/#{ppd}" do
            source ppd_uri
            mode "0644"
            action :nothing
          end.run_action(:create)
        end

        script "install_printer" do
          interpreter "python"
          action :nothing
          user "root"
          code <<-EOH
import cups
import cupshelpers
connection=cups.Connection()
if '#{name}' not in connection.getPrinters().keys():
    drivers = connection.getPPDs(ppd_make_and_model='#{make} #{model}')
    ppd = '#{ppd}'
    if ppd != '':
        for key in drivers.keys():
            if key.startswith('lsb/usr') and key.endswith('#{model}/'+ppd):
                ppd = key

    if ppd == '':
        ppd = drivers.keys()[0]

    connection.addPrinter('#{name}',ppdname=ppd, device='#{uri}')
    printer = cupshelpers.Printer('#{name}',connection)
    printer.setOperationPolicy('#{oppolicy}')
    connection.enablePrinter('#{name}')
    connection.acceptJobs('#{name}')
else:
    print "Printer #{name} already exists"
    print "Change operation policy"
    printer = cupshelpers.Printer('#{name}',connection)
    printer.setOperationPolicy('#{oppolicy}')
    EOH
        end.run_action(:run)

      end
    end

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
      if not e.message.frozen?
        node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
      else
        node.set['job_status'][jid]['message'] = e.message
      end
    end
  ensure
    gecos_ws_mgmt_jobids "printers_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "printers_mgmt"
    end.run_action(:reset)
  end
end
