#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: web_browser
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
require 'chef/mixin/shell_out'
include Chef::Mixin::ShellOut

action :setup do

  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)

      trusty = false
      pkg = shell_out("apt-cache policy libsqlite3-ruby").exitstatus
      if pkg
        trusty = true
      end
      if not trusty
        package 'libsqlite3-ruby' do
          action :nothing
        end.run_action(:install)
      else
        package 'ruby-sqlite3' do
          action :nothing
        end.run_action(:install)
      end

      package 'libsqlite3-dev' do
        action :nothing
      end.run_action(:install)

      package 'libnss3-tools' do
        action :nothing
      end.run_action(:install)

      package 'unzip' do
        action :nothing
      end.run_action(:install)

      gem_depends = [ 'sqlite3' ]
      gem_depends.each do |gem|
        gem_package gem do
          gem_binary("/opt/chef/embedded/bin/gem")
          action :nothing
        end.run_action(:install)
      end

      Gem.clear_paths

      require "sqlite3"

      def plugin_id(username,ext_path,plugin_name,plugin_file,action_to_run)

        plugin_dir_temp = "#{plugin_file}_temp"
        directory plugin_dir_temp do
          owner username
          group username
          action :nothing
        end.run_action(:create)

        bash "extract plugin #{plugin_file}" do
          action :nothing
          user username
          code <<-EOH

            unzip #{plugin_file} -d #{plugin_dir_temp}
          EOH
        end.run_action(:run)

        ruby_block "get plugin id" do
          block do
            file_w_id = ::IO.read("#{plugin_dir_temp}/install.rdf")
            idmatch = file_w_id.match(/<em:id>([^<\/]+)<\/em:id>/)
            str_idmatch = idmatch[0]
            clean_id = str_idmatch.gsub("<em:id>","").gsub("</em:id>","")
            
            if action_to_run == "remove" 
              
              if ::File.directory?("#{ext_path}/#{clean_id}") 
                ::FileUtils.rm_rf("#{ext_path}/#{clean_id}")
              end          
              ::FileUtils.rm_rf(plugin_file)
              ::FileUtils.rm_rf(plugin_dir_temp)
            else
              if !::File.directory?("#{ext_path}/#{clean_id}") 
              ::FileUtils.mv(plugin_dir_temp , "#{ext_path}/#{clean_id}")
              end
            end
          end
        end
      end 

      users = new_resource.users

      users.each_key do |user_key|
        nameuser = user_key 
        username = nameuser.gsub!('###','.')
        user = users[user_key]

        homedir = `eval echo ~#{username}`.gsub("\n","")
        plugins = user.plugins
        bookmarks =  user.bookmarks
      
        profiles = "#{homedir}/.mozilla/firefox/profiles.ini"
      
        profile_dirs = []
        extensions_dirs = []
        sqlitefiles = []

        profiles = "#{homedir}/.mozilla/firefox/profiles.ini"
        if ::File.exist? profiles
          ::File.open(profiles, "r") do |infile|
            while (line = infile.gets)
              aline=line.split('=')
              if aline[0] == 'Path'
                profile_dirs << "#{homedir}/.mozilla/firefox/#{aline[1].chomp}"
                extensions_dirs << "#{homedir}/.mozilla/firefox/#{aline[1].chomp}/extensions"
                sqlitefiles << "#{homedir}/.mozilla/firefox/#{aline[1].chomp}/places.sqlite"
              end
            end
          end

          ## CONFIGS STUFF   
          if !user.config.empty?
            Chef::Log.info("Setting user #{username} web configs")
            arr_conf = []
            user.config.each do |conf|
              value = nil
              if conf[:value_type] == "string"
                value = conf[:value_str]
                if conf[:value_str].nil?
                  raise "The key #{conf[:key]} has no value, Please check it"
                end
              elsif conf[:value_type] == "boolean"
                value = conf[:value_bool]
                if conf[:value_bool].nil?
                  raise "The key #{conf[:key]} has no value, Please check it"
                end
              elsif conf[:value_type] == "number"
                value = conf[:value_num]
                if conf[:value_num].nil?
                  raise "The key #{conf[:key]} has no value, Please check it"
                end
              end
              config = {}
              config['key'] = conf[:key]
              config['value'] = value
              arr_conf << config
            end
     
            profile_dirs.each do |prof|
              template "#{prof}/user.js" do
                owner username
                source "web_browser_user.js.erb"
                variables ({:config => arr_conf})
                action :nothing
              end.run_action(:create)
            end
          end
        
          ## Plugins STUFF
          unless plugins.empty?
            Chef::Log.info("Setting user #{username} web plugins")  
            template "/etc/firefox/pref/web_browser_res.js" do
              source "web_browser_scope.js.erb"
              action :nothing
            end.run_action(:create)
            
            extensions_dirs.each do |xdir|
              directory xdir do
                owner username
                group username
                action :nothing
              end.run_action(:create)
          
              plugins.each do |plugin|
                plugin_name = "#{plugin.name.gsub(" ","_")}.xpi"
                plugin_file = "#{xdir}/#{plugin_name}"
                plugin_dir_temp = "#{plugin_file}_temp"
        
                if !::File.exists?(plugin_file) and plugin.action == "add"
      
                  remote_file plugin_file do
                    source plugin.uri
                    user username
                    group username
                    action :nothing
                  end.run_action(:create)

                  plugin_id(username,xdir,plugin_name,plugin_file,plugin.action)

                elsif ::File.exists?(plugin_file) and plugin.action == "remove"
                  plugin_id(username,xdir,plugin_name,plugin_file,plugin.action)             
                end
              end
            end
          end 

          ## BOOKMARKS STUFF
          Chef::Log.info("Setting user #{username} web bookmarks")     
          sqlitefiles.each do |sqlitedb|
            if ::FileTest.exist? sqlitedb
             db = SQLite3::Database.open(sqlitedb)

              id_folder_bookmarks = db.get_first_value("SELECT id FROM moz_bookmarks WHERE title=\'Marcadores corporativos\'")
              if !id_folder_bookmarks.nil?
                db.execute("delete from moz_bookmarks where parent=#{id_folder_bookmarks} ")
              end
     
              bookmarks.each  do |bkm|
                unless bkm.name.empty? 
                  date_now = Time.now.to_i*1000000
                  url = db.get_first_value("SELECT url FROM moz_places WHERE url LIKE \'#{bkm.uri}\'")
                  if !url.nil?
                    db.execute("delete from moz_places where url LIKE \'#{bkm.uri}\'")
                  end

                  id_toolbar_bookmarks = db.get_first_value("SELECT id FROM moz_bookmarks WHERE title=\'Barra de herramientas de marcadores\'")
                  last_pos_toolbar = db.get_first_value("SELECT MAX(position) FROM moz_bookmarks WHERE parent=#{id_toolbar_bookmarks}")
                  last_pos_folder = 0

                  if id_folder_bookmarks.nil?
                    db.execute("INSERT INTO moz_bookmarks (type,parent,position,title,dateAdded,lastModified) VALUES (2,#{id_toolbar_bookmarks},#{last_pos_toolbar+1},\'Marcadores corporativos\',#{date_now},#{date_now})")
                    id_folder_bookmarks = db.get_first_value("SELECT last_insert_rowid()")
                  else
                    last_pos_folder = db.get_first_value("SELECT MAX(position) FROM moz_bookmarks WHERE id=#{id_folder_bookmarks}")
                  end

                  db.execute("INSERT INTO moz_places (url,title,rev_host,visit_count,hidden,typed,last_visit_date) VALUES  (\'#{bkm.uri}\',\'#{bkm.name}\',\'#{bkm.uri.reverse}.\',1,0,1,#{date_now})")
                   foreign_key = db.get_first_value("SELECT last_insert_rowid()")

                  db.execute("INSERT INTO moz_bookmarks (type,fk,parent,position,title,dateAdded,lastModified) VALUES (1,#{foreign_key},#{id_folder_bookmarks},#{last_pos_folder+1},\'#{bkm.name}\',#{date_now},#{date_now})") 
                end
              end
            end
          end  

               

          ## CERTS STUFF
          #profile_dirs.each do |prof|
          #  user.certs.each do |cert|
          #
          #    certfile = "/var/tmp/#{cert.name}.pem"
          #
          #    remote_file certfile do
          #      source cert.uri
          #      action :nothing
          #    end.run_action(:create_if_missing)
          #
          #    bash "Installing #{cert.name} cert to user #{username}" do
          #      action :nothing
          #      user username
          #      code <<-EOH
          #        certutil -A -d #{prof} -n #{cert.name} -i #{certfile} -t C,C,C
          #      EOH
          #    end.run_action(:run)
          #  end
          #end
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
    gecos_ws_mgmt_jobids "web_browser_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end
