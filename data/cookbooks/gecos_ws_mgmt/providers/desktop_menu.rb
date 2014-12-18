#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: desktop_menu
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#



APPLICATIONS_DIR = "/usr/share/applications/"

# Given a menu/submenu, it checks if each desktop_file belong to it
# and builds the respective include or exclude xml tags
def populate_filename (desktop_files, xdg_menu, action="Exclude")
  result = ""

	# TODO: remove the desktop file from the list once matched to prevent 
	# for checking it again
	desktop_files.each do |desktop_file| 
		xdg_desktop_file = DesktopEntry.new APPLICATIONS_DIR + desktop_file

		# XDG_MENU provides us a method to check if a desktop_file belongs to it
    if xdg_menu.included?(xdg_desktop_file)
      result += "<Filename>#{xdg_desktop_file.info.name}</Filename>"
    end
  end

  # It builds the <Include> or <Exclude> tag with the <Filenames> inside
  if !result.empty?
  	result = "<#{action}>#{result}</#{action}>"
  end	

  return result
end

# WARNING: Recursive function. Handle with care :)
# It walks recursively through the user's menu xml tree 
def populate_menu(to_include, to_exclude, xdg_menu)
  result = ""
  xdg_menu.submenus.each do |menu_entry|

    # This ignore leafs of the xml tree
    if menu_entry.is_a?(SubMenu)

	    	# Add <Filename> tags delegating on the proper function for both
	    	# include and exclude lists
        filenames_xml = populate_filename(to_include, menu_entry, "Include") + populate_filename(to_exclude, menu_entry, "Exclude")

        # If some results were found It builds the proper <Menu><Name> tag
        if !filenames_xml.empty?
          result += "<Menu><Name>#{menu_entry.name}</Name>#{filenames_xml}</Menu>"
        else
          # Walking on the xml tree depth
          menu_xml = populate_menu(to_include, to_exclude, menu_entry)

          # WARNING!! Nasty workaround: once it goes up one level on the recursive 
          # call, this is cheching if the returned value is a String (the produced xml)
          # and not a list of elements of the submenu. Not a smart code, but works.
          if menu_xml.class == String
            if !menu_xml.empty?
              result += "<Menu><Name>#{menu_entry.name}</Name>#{menu_xml}</Menu>"
            end
          end
        end
    end
	end
	return result
end

def user_xdg_menu_preferences(to_include, to_exclude, xdg_menu)
  # XDG_MENU spec HEADER
  header = "<?xml version='1.0' ?><!DOCTYPE Menu PUBLIC '-//freedesktop//DTD Menu 1.0//EN' 'http://standards.freedesktop.org/menu-spec/menu-1.0.dtd'>"

  # Call the recursive building of the XML menu.
  content = populate_menu(to_include, to_exclude, xdg_menu)
  if !content.empty?
    # Append the proper <MergeFile> XML tag. See XDG_MENU SPEC.
    content = "<Menu><Name>#{xdg_menu.name}</Name><MergeFile type='parent'>#{xdg_menu.info.path}</MergeFile>#{content}</Menu>"

    # XML pretty formatting (compress XML and 4 spaces indent)
    result = ""
    doc = REXML::Document.new(header + content)
    formatter = REXML::Formatters::Pretty.new
    formatter.compact = true
    formatter.write(doc, result)
    return result
  end
  return ""
end

action :setup do
  begin
    users = new_resource.users 


    # TODO: Check if this is enough or if it would need some intelligence to get this path
    xdg_menu_name = "cinnamon-applications.menu"

    # It builds the complete user menu as a ruby hash (ruby-xdg menu)
    

    users.each_key do |user_key|
      username = user_key 
      username.gsub!('###','.')
      user = users[user_key]
      ENV['HOME'] = '/home/' + user 
      locale = `cat /etc/locale.gen`
      locale = locale.split()[0]
      ENV['LANG'] = locale
      require "rexml/document"
      require "xdg"
      xdg_menu = Menu.new XDG::CONST::XDG["XDG CONFIG DIRS"][0] + "/menus/" + xdg_menu_name
      xdg_menu.build

      desktop_files_include = user.desktop_files_include
      desktop_files_exclude = user.desktop_files_exclude
      homedir = Etc.getpwnam(username).dir

      # Loads the desktop menu xml file
      preferences_menu_xml = user_xdg_menu_preferences(desktop_files_include, desktop_files_exclude, xdg_menu)

      # If there are some preferences, save them in the proper user config file
      if !preferences_menu_xml.empty?
        gid = Etc.getpwnam(username).gid

        # Create directory if it doesn't exists
        directory "#{homedir}/.config/menus" do
          owner username
          group gid
          recursive true
          action :nothing
        end.run_action(:create)

        file "#{homedir}/.config/menus/#{xdg_menu_name}" do
          owner username
          group gid
          mode 0644
          content preferences_menu_xml
          action :nothing
        end.run_action(:create)

      else # If there isn't any preferences, remove the file
        file "#{homedir}/.config/menus/#{xdg_menu_name}" do
          action :nothing
        end.run_action(:delete)
      end
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
    gecos_ws_mgmt_jobids "desktop_menu_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end
