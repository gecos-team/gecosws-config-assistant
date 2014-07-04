name              "gecos_ws_mgmt"
maintainer        "Roberto C. Morano"
maintainer_email  "rcmorano@emergya.com"
license           "Apache 2.0"
description       "Cookbook for GECOS workstations administration"
version           "0.2.6"

depends "apt"
depends "chef-client"

%w{ ubuntu debian }.each do |os|
  supports os
end

# more complete input definition via json-schemas:

updated_js = {
  title: "Updated by",
  type: "object",
  properties: {
    group: {title: "Groups", type: "array", items: {type:"string"}},
    user: {title: "Users", type: "array", items: {type:"string"}},
    computer: {type:"string"},
    ou: {title: "Ous", type: "array", items: {type:"string"}}
  }
}
    

sssd_js = {
  title: "Authenticate System",
  type: "object",
  required: ["auth_type", "enabled"],
  properties: {
    krb_url: { type: "string" , title: "Url Kerberos file configuration"},
    smb_url: { type: "string" , title: "Url Samba file configuration" },
    sssd_url: { type: "string" , title: "Url SSSD file configuration" },
    domain_list: {
      type:"array",
      items: {
        type:"object",
        required: ["domain_name"],
        properties: {
          domain_name: {pattern: "(?=^.{1,254}$)(^(?:(?!\\d+\\.)[a-zA-Z0-9_\\-]{1,63}\\.?)+(?:[a-zA-Z]{2,})$)", type: "string", title: "Domain name"}
        }
      }
    },
    workgroup: {
        title: "Workgroup",
        type: "string"
    },
    enabled: {
      title: "Enabled",
      type: "boolean", default: false
    },
    auth_type:{
      title: "Authenticate type",
      type: "string"
    },
    uri:{
      title: "LDAP Uri",
      type: "string"
    },
    basegroup:{
      title: "Base Group",
      type: "string"
    },
    base:{
      title: "Search Base",
      type: "string"
    },
    basegroup:{
      title: "Base Group",
      type: "string"
    },
    binddn:{
      title: "BindDN",
      type: "string"
    },
    bindpwd:{
      title: "Bin Password",
      type: "string"
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }, 
    updated_by: updated_js
  }
}

user_mount_js = {
  title: "User mount extern units",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["can_mount"],
          properties: {
            can_mount: {type: "boolean", title: "Can Mount?"}, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }
  }
}

screensaver_js = {
  title: "Screensaver",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["idle_enabled", "lock_enabled"],
          properties: {
            idle_enabled: {
              type: "boolean",
              title: "Idle Enabled?"
            },
            idle_delay: {
              type: "string",
              title: "Idle Delay"
            },
            lock_enabled: {
              type: "boolean",
              title: "Lock Enabled?"
            },
            lock_delay: {
              type: "string",
              title: "Lock Delay"
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }
  }
}

folder_sharing_js = {
  title: "Sharing permissions",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["can_share"],
          properties: {
            can_share: {title: "Can Share?", type: "boolean"}, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}

desktop_control_js = {
  title: "Desktop Control",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["desktop_files"],
          properties: {
            desktop_files: {
              type: "array",
              title: "Desktop Files",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "string"
              }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}


desktop_menu_js = {
  title: "Desktop Menu",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["desktop_files_include", "desktop_files_exclude"],
          properties: {
            desktop_files_include: {
              type: "array",
              title: "Desktop Files to include",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "string"
              }
            },
            desktop_files_exclude: {
              type: "array",
              title: "Desktop Files to exclude",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "string"
              }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}

user_launchers_js = {
  title: "User Launchers",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["launchers"],
          properties: {
            launchers: {
              type: "array",
              title: "Launchers",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "string"
              }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}

#desktop_background_js = {
#  title: "Desktop Background",
#  type: "object",
#  required: ["desktop_file"],
#  properties: {
#    desktop_file: {type: "string", title: "Desktop File"},
#    job_ids: {
#      type: "array",
#      minItems: 0,
#      uniqueItems: true,
#      items: {
#        type: "string"
#      }
#    }, 
#    updated_by: updated_js
#  }
#}
desktop_background_js = {
  type: "object",
  title: "Desktop Background",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["desktop_file"],
          properties: {
            desktop_file: {type: "string", title: "Desktop File"},
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string",
        }
    }
  }
}


file_browser_js = {
  title: "File Browser",
  type: "object",
  required: ["users"],
  properties:{
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["default_folder_viewer", "show_hidden_files", "show_search_icon_toolbar", "click_policy", "confirm_trash"],
          properties: {
            default_folder_viewer: {type: "string", title: "Folder viewer", enum: ["icon-view", "compact-view", "list-view"], default: "icon-view"},
            show_hidden_files: {type: "string", title: "Show hidden files?", enum: ["true","false"], default: "false"},
            show_search_icon_toolbar: {type: "string", title: "Show search icon on toolbar?", enum: ["true", "false"], default: "true"},
            confirm_trash: {type: "string", title: "Confirm trash?", enum: ["true","false"], default: "true"},
            click_policy: {type: "string", title: "Click policy", enum: ["single", "double"], default: "double"}, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}






web_browser_js = {
  title: "Web Browser",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "object",
      title: "Users",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          properties: {
            plugins: {
              type: "array",
              title: "Plugins", 
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["name", "uri", "action"],
                properties: {
                  name: {title: "Name", type: "string"},
                  uri: {title: "Uri", type: "string"},
                  action: {title: "Action", type: "string", enum: ["add", "remove"]}
                }
              }
            },
            bookmarks: {
              type: "array",
              title: "Bookmarks",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["name", "uri"],
                properties: {
                  name: {title: "Name", type: "string"},
                  uri: {title: "Uri", type: "string"}
                }
              }
            },
            config: {
              type: "array",
              title: "Configs",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["key", "value"],
                properties: {
                  key: {type: "string", title: "Key"},
                  value: {type: ["string","boolean","number"], title: "Value"}
                }
              }
            },
            certs: {
              type: "array",
              title: "Certificates",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: [ "name", "uri"],
                properties: {
                  name: {title: "Name", type: "string"},
                  uri: {title: "Uri", type: "string"}
                }
              }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}

user_shared_folders_js = {
  title: "Shared Folders",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["gtkbookmarks"],
          properties: {
            gtkbookmarks: {
              type: "array",
              title: "Bookmarks", 
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["name", "uri"],
                properties: {
                  name: {title: "Name", type: "string"},
                  uri: {title: "Uri", type: "string"}
                }
              }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}

app_config_js = {
  title: "Applications Config",
  type: "object",
  required: ["adobe_config", "java_config", "firefox_config", "thunderbird_config"],
  properties: {
    adobe_config: {title: "Adobe Configuration", type: "object"},
    java_config: {title: "Java Configuration", type: "object"},
    firefox_config: {title: "Firefox Configuration", type: "object"},
    thunderbird_config: {title: "Thuderbird Configuration", type: "object"},
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }, 
    updated_by: updated_js
  }
}

auto_updates_js = {
  title: "Automatic Updates",
  type: "object",
  required: ["auto_updates_rules"],
  properties: {
    auto_updates_rules: {
      type: "object",
      title: "Auto Updates Rules",
      required: ["onstop_update", "onstart_update", "days"],
      properties: {
        onstop_update: {title: " On stop Update?", type: "boolean"},
        onstart_update: {title: "On start Update?", type: "boolean"},
        days: {
          type: "array",
          title: "Days",
          minItems: 0,
          uniqueItems: true,
          items: {
            type: "object",
            required: ["day", "hour", "minute"],
            properties: {
              day: {
                title: "Day",
                type: "string",
                enum: ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
              },
              hour: {
                title: "Hour",
                type: "integer",
                maximum: 23
              },
              minute: {
                title: "Minute",
                type: "integer",
                maximum: 59
              }

            }
          }
        },
        date: {
          title: "Date",
          type: "object",
          properties: {
            day: {title: "Day", type: "integer", maximum: 31},
            month: {title: "Month", type: "integer", maximum: 12},
            hour: {title: "Hour", type: "integer", maximum: 23},
            minute: {title: "Minute", type: "integer", maximum: 59}
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }, 
    updated_by: updated_js
  }
}


user_apps_autostart_js = {
  title: "Autostart applications",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["desktops"],
          properties: {
            desktops: {
              title: "Desktops",
              type: "array",
              minItems: 0,
              uniqueItems: true,
              items: {type: "string"}
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }
  }
}

tz_date_js = {
  title: "Date/Time Manager",
  type: "object",
  required: ["server"],
  properties: {
    server: {
      type: "string",
      title: "Server"
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "string"
        }
    }, 
    updated_by: updated_js
  }
}

scripts_launch_js = {
  title: "Scripts Launcher",
  type: "object",
  required: ["on_startup","on_shutdown"],
  properties:
  {
    on_startup: {
      type: "array",
      title: "Script list to run on startup",
      minItems: 0,
      uniqueItems: false,
      items: {
        type: "string",
        }
    },
    on_shutdown: {
      type: "array",
      title: "Script list to run on shutdown",
      minItems: 0,
      uniqueItems: false,
      items: {
        type: "string",
        }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }, 
    updated_by: updated_js
  }
}

network_resource_js = {
  title: "Network Manager",
  type: "object",
  required: ["network_type", "dns_servers_array"],
  properties:
  {
    gateway: { type: "string",title: "Gateway" },
    ip_address: { type:"string", title: "Ip Address" },
    netmask: { type: "string", title: "Netmask" },
    network_type: { enum: ["wired","wireless"],type: "string", title: "Network Type" },
    use_dhcp: { type: "boolean" , title: "Use DHCP?"},
    dns_servers_array: {
      type: "array",
      title: "DNS Servers",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    },
#    users: {
#      type: "object",
#      title: "Users",
#      patternProperties: {
#        ".*" => { type: "object", title: "Username",
#          required: ["network_type"],
#          properties: {
#            username: { type: "string", title: "Username" },
#            gateway: { type: "string",title: "Gateway" },
#            ip_address: { type:"string", title: "Ip Address" },
#            netmask: { type: "string", title: "Netmask" },
#            network_type: { enum: ["wired","wireless","vpn","proxy"], type: "string", title: "Network Type" },
#            use_dhcp: { type: "boolean", title: "Use DHCP?" },
#            certs: {
#              type: "array",
#              title: "Certificates",
#              minItems: 0,
#              uniqueItems: true,
#              items: {
#                type: "object",
#                required: ["name","uri"],
#                properties: {
#                  name: {type: "string", title: "Name"},
#                  uri: {type: "string", title: "Url"}
#                }
#              }
#            }
#          }
#        }
#      }
#    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }, 
    updated_by: updated_js
  }
}

software_sources_js = {
  title: "Software Sources",
  type: "object",
  required: ["repo_list"],
  properties:{
    repo_list: {
      type:"array",
      items: {
        type:"object",
        required: ["repo_name","distribution","components","uri","deb_src","repo_key","key_server"],
        properties:{
          components: { title: "Components", type: "array",items: { type: "string" } },
          deb_src: { title: "Sources", type: "boolean", default: false },
          repo_key: { title: "Repository key", type: "string", default: ""},
          key_server: { title: "Server key", type: "string", default: ""},
          distribution: { title: "Distribution", type: "string"},
          repo_name: { title: "Repository name", type: "string"},
          uri: { title: "Uri", type: "string" }
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }, 
    updated_by: updated_js
   }
}


package_js = {
  title: "Packages",
  type: "object",
  properties:
  {
    package_list: {
      type:"array",
      title: "Package list to install",
      minItems: 0,
      uniqueItems: true,
      items: {type: "string"}
    },
    pkgs_to_remove: {
      type:"array",
      title: "Package list to remove",
      minItems: 0,
      uniqueItems: true,
      items: {type: "string"}
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    },
    updated_by: updated_js
  }
}

printers_js = {
  title: "Printers",
  type: "object",
  required: ["printers_list"],
  properties:
  {
    printers_list: {
      type:"array",
      title: "Printer list to enable",
      items: {
        type:"object",
        required: [ "name", "manufacturer", "model", "ppd_uri" ],
        properties:{
          name: { type: "string", title: "Name" },
          manufacturer: { type: "string", title: "Manufacturer" },
          model: { type: "string" , title: "Model"},
          uri: { type: "string", title: "Uri" },
          ppd_uri: { type: "string", title: "Uri PPD", default: ""},
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }, 
    updated_by: updated_js
  }
}

local_users_js = {
  title: "Local users",
  type: "object",
  required: ["users_list"],
  properties:
  {users_list: {
      type:"array",
      title: "User list to manage",
      items: {
        type:"object",
        required: ["user","actiontorun"],
        properties:{
          actiontorun: {enum: ["create","modify","delete"],type: "string"},
          groups: { title: "Groups", type: "array",items: { type: "string" } },
          user: { title: "User", type: "string" },
          name: { title: "Full Name", type: "string" },
          password: { title: "Password", type: "string"}
        }
     }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "string"
    }
  }, 
  updated_by: updated_js
 }
}

local_groups_js = {
  title: "Local groups",
  type: "object",
  required: ["groups_list"],
  properties:
  {groups_list: {
      type:"array",
      title: "Group List to manage",
      items: {
        type:"object",
        required: ["group"],
        properties:{
          group: { type: "string", title: "Group" },
          users: { type: "array",title: "Users", items: { type: "string" } }
        }
     }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "string"
    }
  }, 
  updated_by: updated_js
 }
}

local_file_js = {
  title: "Local files",
  type: "object",
  required: ["delete_files", "copy_files"],
  properties:
  {delete_files: {
      type:"array",
      title: "File list to delete",
      items: {
        type:"object",
        required: ["file"],
        properties:{
          file: {type: "string", title:"File"},
          backup: { type: "boolean", title: "Create backup?" }
        }
     }
  },
  copy_files: {
    type: "array",
    title: "File list to copy",
    items: {
      type: "object",
      required: ["file_orig","file_dest"],
      properties:{
        file_orig: {type: "string", title: "Url File"},
        file_dest: {type: "string", title: "Path destination"},
        user: {type: "string", title:"User"},
        group: {type: "string", title: "Group"},
        mode: {type: "string", title: "Mode"},
        overwrite: {type: "boolean", title: "Overwrite?"}
      }
    }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "string"
    }
  }, 
  updated_by: updated_js
 }
}

local_admin_users_js = {
  title: "Local Admin Users",
  type: "object",
  required: ["local_admin_list"],
  properties:
  {local_admin_list: {
      type:"array",
      title: "Local users to grant admin permissions", 
      items: { type:"string"}
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "string"
    }
  }, 
  updated_by: updated_js
 }
}

folder_sync_js = {
  title: "Folder to sync",
  type: "object",
  required: ["users"],
  properties:
  {users: {
    title: "Users", 
    type: "object",
    patternProperties: {
      ".*" => { type: "object", title: "Username",
        required: ["remote_folders"],
        properties: {
          username: {title: "Username", type: "string"},
          remote_folders: {
            type: "array",
            title: "Remote Folders",
            items: {type: "string"},
            minItems: 0,
            uniqueItems:true
          }, 
          updated_by: updated_js
        }
      }
    }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "string"
    }
  }
 }
}

power_conf_js = {
  title: "Power management",
  type: "object",
  required: ["cpu_freq_gov","auto_shutdown","usb_autosuspend"],
  properties:
    {cpu_freq_gov: {
       title: "CPU frequency governor", 
       type: "string",
       enum: ["userspace","powersave","conservative","ondemand","performance",""]
       },
    usb_autosuspend: 
      {
       title: "USB autosuspend",
       type: "string",  
       enum: ["enable","disable", ""]
       },
     auto_shutdown: {
       type: "object",
       properties: {
         hour: {
           title: "Hour",
           type: "integer",
           maximum: 23
           },
         minute: {
           title: "Minute",                                                                                                                                                                                     
           type: "integer",
           maximum: 59
         }
       }  
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "string"
    }
  }, 
  updated_by: updated_js
 }
}

shutdown_options_js = {
  title: "Shutdown Options",
  type: "object",
  required: ["users"],
  properties: { 
    systemlock: { type: "boolean", title: "System-wide lockdown of the key" },
    users: {
      type: "object", 
      title: "Users",
      patternProperties: {
        ".*" => { type: "object", title: "Username",
          required: ["disable_log_out"],
          properties:{
            disable_log_out: {
              title: "Disable log out?",
              type: "boolean",
              default: false
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    }
 }
}

complete_js = {
  description: "GECOS workstation management LWRPs json-schema",
  id: "http://gecos-server/cookbooks/#{name}/#{version}/network-schema#",
  required: ["gecos_ws_mgmt"],
  type: "object",
  properties: {
    gecos_ws_mgmt: {
      type: "object",
      required: ["network_mgmt","software_mgmt", "printers_mgmt", "misc_mgmt", "users_mgmt"],
      properties: {
        network_mgmt: {
          type: "object",
          required: ["network_res"],
          properties: {
            network_res: network_resource_js
            #sssd_res: sssd_js
          }
        },
        misc_mgmt: {
          type: "object",
          required: ["tz_date_res", "scripts_launch_res", "local_users_res", "local_groups_res", "local_file_res", "local_admin_users_res", "auto_updates_res","power_conf_res"],
          properties: {
            tz_date_res: tz_date_js,
            scripts_launch_res: scripts_launch_js,
            local_users_res: local_users_js,
            local_file_res: local_file_js,
           # desktop_background_res: desktop_background_js,
            auto_updates_res: auto_updates_js,
            local_groups_res: local_groups_js,
            power_conf_res: power_conf_js,
            local_admin_users_res: local_admin_users_js
          }
        },
        software_mgmt: {
          type: "object",
          required: ["software_sources_res","package_res", "app_config_res"],
          properties: {
            software_sources_res: software_sources_js,
            package_res: package_js,
            app_config_res: app_config_js
          }
        },
        printers_mgmt: {
          type: "object",
          required: ["printers_res"],
          properties: {
            printers_res: printers_js
          }
        },
        users_mgmt: {
          type: "object",
          required: ["user_apps_autostart_res", "user_shared_folders_res", "web_browser_res", "file_browser_res", "user_launchers_res", "desktop_menu_res", "desktop_control_res", "folder_sharing_res", "screensaver_res","folder_sync_res", "user_mount_res","shutdown_options_res","desktop_background_res"],
          properties: {
            user_shared_folders_res: user_shared_folders_js,
            web_browser_res: web_browser_js,
            file_browser_res: file_browser_js,
            user_launchers_res: user_launchers_js,
            desktop_background_res: desktop_background_js,
            desktop_menu_res: desktop_menu_js,
            desktop_control_res: desktop_control_js,
            user_apps_autostart_res: user_apps_autostart_js,
            folder_sharing_res: folder_sharing_js,
            screensaver_res: screensaver_js,
            folder_sync_res: folder_sync_js,
            user_mount_res: user_mount_js,
            shutdown_options_res: shutdown_options_js
          }
        }
      }
    }
  }
}

attribute 'json_schema',
  :display_name => "json-schema",
  :description  => "Special attribute to include json-schema for defining cookbook's input",
  :type         => "hash",
  :object       => complete_js
