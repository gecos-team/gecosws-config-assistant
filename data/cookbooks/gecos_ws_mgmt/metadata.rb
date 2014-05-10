name              "gecos_ws_mgmt"
maintainer        "Roberto C. Morano"
maintainer_email  "rcmorano@emergya.com"
license           "Apache 2.0"
description       "Cookbook for GECOS workstations administration"
version           "0.2.3"

depends "apt"
depends "chef-client"

%w{ ubuntu debian }.each do |os|
  supports os
end

# more complete input definition via json-schemas:

sssd_js = {
  type: "object",
  required: ["domain_list", "workgroup"],
  properties: {
    krb_url: { type: "string" },
    smb_url: { type: "string" },
    sssd_url: { type: "string" },
    domain_list: {
      type:"array",
      items: {
        type:"object",
        required: ["domain_name"],
        properties: {
          domain_name: {pattern: "(?=^.{1,254}$)(^(?:(?!\\d+\\.)[a-zA-Z0-9_\\-]{1,63}\\.?)+(?:[a-zA-Z]{2,})$)", type: "string"}
        }
      }
    },
    workgroup: {
        type: "string"
    },
    enabled: {
      type: "boolean", default: false
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["id"],
        properties: {
          id: { type: "string" },
          status: { type: "string" }
        }
      }
    }
  }
}

user_mount_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username","can_mount"],
        properties: {
          username: {type: "string"},
          can_mount: {type: "boolean"}
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["id"],
        properties: {
          id: { type: "string" },
          status: { type: "string" }
        }
      }
    }
  }
}

screensaver_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username", "idle_enabled", "lock_enabled"],
        properties: {
          username: {
            type: "string"
          },
          idle_enabled: {
            type: "boolean"
          },
          idle_delay: {
            type: "string"
          },
          lock_enabled: {
            type: "boolean"
          },
          lock_delay: {
            type: "string"
          }
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["id"],
        properties: {
          id: { type: "string" },
          status: { type: "string" }
        }
      }
    }
  }
}

folder_sharing_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItem: 0,
      uniqueItem: true,
      items: {
        type: "object",
        required: ["username", "can_share"],
        properties: {
          username: {type: "string"},
          can_share: {type: "boolean"}
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

desktop_control_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItem: 0,
      uniqueItem: true,
      items: {
        type: "object",
        required: ["username", "desktop_files"],
        properties: {
          username: {type: "string"},
          desktop_files: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "string"
            }
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}


desktop_menu_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItem: 0,
      uniqueItem: true,
      items: {
        type: "object",
        required: ["username", "desktop_files"],
        properties: {
          username: {type: "string"},
          desktop_files: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "string"
            }
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

user_launchers_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items:{
        type: "object",
        required: ["username", "launchers"],
        properties: {
          username: {type: "string"},
          launchers: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "string"
            }
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

desktop_background_js = {
  type: "object",
  required: ["desktop_file"],
  properties: {
    desktop_file: {type: "string", title: "Desktop File"}
  },
  job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
  }
}
#desktop_background_js = {
#  type: "object",
#  required: ["users"],
#  properties: {
#    users: {
#      type: "array",
#      minItems: 0,
#      uniqueItems: true,
#      items: {
#        type: "object",
#        required: ["username", "desktop_file"],
#        properties: {
#          username: {type: "string"},
#          desktop_file: {type: "string"}
#        }
#      }
#    },
#    job_ids: {
#        type: "array",
#        minItems: 0,
#        uniqueItems: true,
#        items: {
#          type: "object",
#          required: ["id"],
#          properties: {
#            id: { type: "string" },
#            status: { type: "string" }
#          }
#        }
#    }
#  }
#}
#

file_browser_js = {
  type: "object",
  required: ["users"],
  properties:{
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username", "auto_mount", "explore_net", "show_options_mount", "burn_disc"],
        properties: {
          user: {type: "string"},
          auto_mount: {type: "boolean"},
          explore_net: {type: "boolean"},
          show_options_mount: {type: "boolean"},
          burn_disc: {type: "boolean"}
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}






web_browser_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username"],
        properties: {
          username: {type: "string"},
          plugins: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "object",
              required: ["title", "uri", "action"],
              properties: {
                title: {type: "string"},
                uri: {type: "string"},
                action: {type: "string" ,pattern: "(add|remove)"}
              }
            }
          },
          bookmarks: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "object",
              required: ["title", "uri"],
              properties: {
                title: {type: "string"},
                uri: {type: "string"}
              }
            }
          },
          config: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "object",
              required: ["key", "value"],
              properties: {
                key: {type: "string"},
                value: {type: "any"}
              }
            }
          },
          certs: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "object",
              required: [ "name", "uri"],
              properties: {
                name: {type: "string"},
                uri: {type: "string"}
              }
            }
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

user_shared_folders_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username", "gtkbookmarks"],
        properties: {
          username: {type: "string"},
          gtkbookmarks: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "object",
              required: ["title", "uri"],
              properties: {
                title: {type: "string"},
                uri: {type: "string"}
              }
            }
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

app_config_js = {
  type: "object",
  required: ["adobe_config", "java_config", "firefox_config", "thunderbird_config"],
  properties: {
    adobe_config: {type: "object"},
    java_config: {type: "object"},
    firefox_config: {type: "object"},
    thunderbird_config: {type: "object"},
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

auto_updates_js = {
  type: "object",
  required: ["auto_updates_rules"],
  properties: {
    auto_updates_rules: {
      type: "object",
      required: ["logout_update", "start_update", "days"],
      properties: {
        logout_update: {type: "boolean"},
        start_update: {type: "boolean"},
        days: {
          type: "array",
          minItems: 0,
          uniqueItems: true,
          items: {
            type: "object",
            required: ["day", "hour", "period"],
            properties: {
              day: {
                type: "string",
                pattern: "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
              },
              hour: {
                type: "integer",
                pattern: "[0-12]"
              },
              period: {
                type: "string",
                pattern: "(am|pm)"
              }
            }
          }
        },
        date: {
          type: "object",
          required: ["day", "month", "year"],
          properties: {
            day: {type: "integer", maximum: 31},
            month: {type: "integer", maximum: 12},
            year: {type: "integer"}
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}


user_apps_autostart_js = {
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username", "desktops"],
        properties: {
          username: {type: "string"},
          desktops: {
            type: "array",
            minItems: 0,
            uniqueItems: true,
            items: {type: "string"}
          }
        }
      }
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

tz_date_js = {
  type: "object",
  required: ["server"],
  properties: {
    server: {
      type: "string"
    },
    job_ids: {
        type: "array",
        minItems: 0,
        uniqueItems: true,
        items: {
          type: "object",
          required: ["id"],
          properties: {
            id: { type: "string" },
            status: { type: "string" }
          }
        }
    }
  }
}

scripts_launch_js = {
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
        type: "object",
        required: ["id"],
        properties: {
          id: { type: "string" },
          status: { type: "string" }
        }
      }
    }
  }
}

network_resource_js = {
  type: "object",
  required: ["network_type", "dns_servers"],
  properties:
  {
    gateway: { type: "string",title: "Gateway" },
    ip_address: { type:"string", title: "Ip Address" },
    netmask: { type: "string", title: "Netmask" },
    network_type: { enum: ["wired","wireless"],type: "string", title: "Network Type" },
    use_dhcp: { type: "boolean" , title: "Use DHCP?"},
    dns_servers: {
      type: "array",
      title: "DNS Servers",
      minItems: 1,
      uniqueItems: true,
      items: {
        type: "string"
      }
    },
    users: {
      type: "array",
      title: "Users",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["username","network_type"],
        properties: {
          username: { type: "string", title: "Username" },
          gateway: { type: "string",title: "Gateway" },
          ip_address: { type:"string", title: "Ip Address" },
          netmask: { type: "string", title: "Netmask" },
          network_type: { enum: ["wired","wireless","vpn","proxy"], type: "string", title: "Network Type" },
          use_dhcp: { type: "boolean", title: "Use DHCP?" },
          certs: {
            type: "array",
            title: "Certificates",
            minItems: 0,
            uniqueItems: true,
            items: {
              type: "object",
              required: ["name","uri"],
              properties: {
                name: {type: "string", title: "Name"},
                uri: {type: "string", title: "Url"}
              }
            }
          }
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["id"],
        properties: {
          id: { type: "string" },
          status: { type: "string" }
        }
      }
    }
  }
}

software_sources_js = {
  type: "object",
  required: ["repo_list"],
  properties:
  {repo_list: {
      type:"array",
      items: {
        type:"object",
        required: ["repo_name","distribution","components","uri","deb_src","repo_key","key_server"],
        properties:{
          components: { type: "array",items: { type: "string" } },
          deb_src: { type: "boolean", default: false },
          repo_key: { type: "string", default: ""},
          key_server: { type: "string", default: ""},
          distribution: { type: "string"},
          repo_name: { type: "string"},
          uri: { type: "string" }
        }
     }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

package_js = {
  type: "object",
  properties:
  {package_list: {
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
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

printers_js = {
  type: "object",
  required: ["printers_list"],
  properties:
  {
    printers_list: {
      type:"array",
      items: {
        type:"object",
        required: [ "name", "manufacturer", "model", "ppd", "ppd_uri" ],
        properties:{
          name: { type: "string" },
          manufacturer: { type: "string" },
          model: { type: "string" },
          uri: { type: "string" },
          ppd: { type: "string", default: ""},
          ppd_uri: { type: "string", default: ""},
        }
      }
    },
    job_ids: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["id"],
        properties: {
          id: { type: "string" },
          status: { type: "string" }
        }
      }
    }
  }
}

local_users_js = {
  type: "object",
  required: ["users_list"],
  properties:
  {users_list: {
      type:"array",
      items: {
        type:"object",
        required: ["user","actiontorun"],
        properties:{
          actiontorun: {pattern: "(create|modify|delete)",type: "string"},
          groups: { type: "array",items: { type: "string" } },
          user: { type: "string" },
          password: { type: "string"}
        }
     }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

local_groups_js = {
  type: "object",
  required: ["groups_list"],
  properties:
  {groups_list: {
      type:"array",
      items: {
        type:"object",
        required: ["group"],
        properties:{
          group: { type: "string" },
          users: { type: "array",items: { type: "string" } }
        }
     }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

local_file_js = {
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
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

local_admin_users_js = {
  type: "object",
  required: ["local_admin_list"],
  properties:
  {local_admin_list: {
      type:"array",
      items: { type:"string"}
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

folder_sync_js = {
  type: "object",
  required: ["folder_sync"],
  properties:
  {users: {
    type: "array",
    items: {
      type: "object",
      required: ["username","remote_folders"],
      properties:{
        username: {type: "string"},
        remote_folders: {
          type: "array",
          items: {type: "string"},
          minItems: 0,
          uniqueItems:true
        }
      }
    }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
    }
   }
 }
}

shutdown_options_js = {
  type: "object",
  required: ["users"],
  properties:
  {users: {
    type: "array",
    items: {
      type: "object",
      required: ["username","options"],
      properties:{
        username: {type: "string"},
        options: {type: "array",items:{pattern: "(shutdown|restart|close_session)",type:"string"}}
      }
    }
  },
  job_ids: {
    type: "array",
    minItems: 0,
    uniqueItems: true,
    items: {
      type: "object",
      required: ["id"],
      properties: {
        id: { type: "string" },
        status: { type: "string" }
      }
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
            network_res: network_resource_js,
            sssd_res: sssd_js
          }
        },
        misc_mgmt: {
          type: "object",
          required: ["tz_date_res", "desktop_background_res", "scripts_launch_res", "local_users_res", "local_groups_res", "local_file_res", "local_admin_users_res", "auto_updates_res"],
          properties: {
            tz_date_res: tz_date_js,
            scripts_launch_res: scripts_launch_js,
            local_users_res: local_users_js,
            local_file_res: local_file_js,
            desktop_background_res: desktop_background_js,
            auto_updates_res: auto_updates_js,
            local_groups_res: local_groups_js,
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
          required: ["user_apps_autostart_res", "user_shared_folders_res", "web_browser_res", "file_browser_res", "user_launchers_res", "desktop_menu_res", "desktop_control_res", "folder_sharing_res", "screensaver_res","folder_sync_res", "user_mount_res","shutdown_options_res"],
          properties: {
            user_shared_folders_res: user_shared_folders_js,
            web_browser_res: web_browser_js,
            file_browser_res: file_browser_js,
            user_launchers_res: user_launchers_js,
            #desktop_background_res: desktop_background_js,
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
