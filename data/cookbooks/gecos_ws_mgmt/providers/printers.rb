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
        Chef::Log.info("Instalando impresora #{printer.name}")
  
        name = printer.name
        make = printer.manufacturer
        model = printer.model
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
connection=cups.Connection()
drivers = connection.getPPDs(ppd_make_and_model='#{make} #{model}')
ppd = '#{ppd}'
if ppd != '':
    for key in drivers.keys():
        if key.startswith('lsb/usr') and key.endswith('#{model}/'+ppd):
            ppd = key

if ppd == '':
    ppd = drivers.keys()[0]

connection.addPrinter('#{name}',ppdname=ppd, device='#{uri}')
connection.enablePrinter('#{name}')
connection.acceptJobs('#{name}')

    EOH
        end.run_action(:run)

      end
    end
    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end
  rescue
    # TODO:
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

