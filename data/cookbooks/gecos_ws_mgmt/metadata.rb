#encoding:UTF-8
name              "gecos_ws_mgmt"
maintainer        "GECOS Team"
maintainer_email  "gecos@guadalinex.org"
license           "Apache 2.0"
description       "Cookbook for GECOS workstations administration"
version           "0.3.12"

depends "apt"
depends "chef-client"

%w{ ubuntu debian }.each do |os|
  supports os
end

# better fields definition via json-schemas:

updated_js = {
  title: "Updated by",
  title_es: "Actualizado por",
  type: "object",
  properties: {
    group: {title: "Groups", title_es: "Grupos", type: "array", items: {type:"string"}},
    user: {type:"string"},
    computer: {type:"string"},
    ou: {title: "Ous", title_es: "Ous", type: "array", items: {type:"string"}}
  }
}

support_os_js = {
  title: "Supported OS",
  title_es: "Sistemas operativos compatibles",
  type: "array",
  minItems: 0,
  uniqueItems: true,
  items: {
    type: "string"
  }

}

mobile_broadband_js = {
  title: "Mobile broadband connections",
  title_es: "Conexiones de banda ancha móvil",
  type: "object",
  required: ["connections"],
  properties: {
    connections: {
      title: "Connections",
      title_es: "Conexiones",
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        title: "Provider",
        title_es: "Proveedor",
        required: ["provider", "country"],
        order: ["provider","country"],
        properties: { 
          provider: {
            type: "string",
            title: "Provider",
            title_es: "Proveedor",
            enum: ['Euskaltel','Másmovil','móbil R (Mundo-R)','moviData','ONO','Pepephone','Orange','Simyo/Blau','Telecable','Movistar (Telefónica)','Vodafone (Airtel)','Yoigo','Jazztel','Carrefour Móvil','Eroski Móvil'], 
          },
          country: {
            type: "string",
            title: "Country code",
            title_es: "Código de país",
            enum: ["es"]
          }
            
        }
      }
    },
    updated_by: updated_js,
    support_os: support_os_js.clone,
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
    
forticlientvpn_js = {
  title: "FortiClient VPN connections",
  title_es: "Conexiones VPN de FortiClient",
  type: "object",
  required: ["connections"],
  order: ["connections", "proxyserver", "proxyport", "proxyuser", "autostart", "keepalive"],
  properties: {
    connections: {
      title: "Connections",
      title_es: "Conexiones",
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["name", "server", "port"],
        order: ["name", "server", "port"],
        properties: {
          server: {
            type: "string",
            title: "Server",
            title_es: "Servidor"
          },
          port: {
            type: "string",
            title: "Port",
            title_es: "Puerto"
          },
          name: {
            type: "string",
            title: "Name",
            title_es: "Nombre"
          }
        }
      }
    },
    proxyserver:{ 
      type: "string",
      title: "Proxy Server",
      title_es: "Servidor Proxy"
    },
    proxyport: {
      type: "string",
      title: "Proxy Port",
      title_es: "Puerto del Proxy"
    },
    proxyuser: {
      type: "string",
      title: "Proxy user",
      title_es: "Usuario del Proxy"
    },
    autostart: {
      type: "boolean",
      title: "Proxy user",
      default: false,
      title_es: "Arranque automatico"
    },
    keepalive:{ 
      title: "Keepalive frequency",
      title_es: "Frecuencia del keepalive",
      type: "integer"
    },
    updated_by: updated_js,
    support_os: support_os_js.clone,
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


sssd_js = {
  title: "Authenticate System",
  title_es: "Sistema de Autenticación",
  type: "object",
  required: ["auth_type", "enabled"],
  properties: {
    krb_url: { type: "string" , title: "Url of Kerberos file configuration", title_es: "Archivo de configuración Url Kerberos"},
    smb_url: { type: "string" , title: "Url of Samba file configuration", title_es: "Archivo de configuración Url Samba"},
    sssd_url: { type: "string" , title: "Url of SSSD file configuration", title_es: "Archivo de configuración Url SSSD"},
    domain_list: {
      type:"array",
      items: {
        type:"object",
        required: ["domain_name"],
        properties: {
          domain_name: {pattern: "(?=^.{1,254}$)(^(?:(?!\\d+\\.)[a-zA-Z0-9_\\-]{1,63}\\.?)+(?:[a-zA-Z]{2,})$)", type: "string", title: "Domain name", title_es: "Nombre de dominio"}
        }
      }
    },
    workgroup: {
        title: "Workgroup",
        title_es: "Grupo de trabajo",
        type: "string"
    },
    enabled: {
      title: "Enabled",
      title_es: "Habilitado",
      type: "boolean", default: false
    },
    auth_type:{
      title: "Authenticate type",
      title_es: "Tipo de Autenticación",
      type: "string"
    },
    uri:{
      title: "LDAP Uri",
      title_es: "Uri LDAP",
      type: "string"
    },
    basegroup:{
      title: "Base Group",
      title_es: "Grupo de base",
      type: "string"
    },
    base:{
      title: "Search Base",
      title_es: "Grupo de búsqueda",
      type: "string"
    },
    basegroup:{
      title: "Base Group",
      title_es: "Grupo de base",
      type: "string"
    },
    binddn:{
      title: "BindDN",
      title_es: "BindDN",
      type: "string"
    },
    bindpwd:{
      title: "Bin Password",
      title_es: "Bin contraseña",
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

user_mount_js = {
  title: "User mount external units",
  title_es: "Montaje de unidades externas",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["can_mount"],
          properties: {
            can_mount: {type: "boolean", title: "Can Mount?", title_es: "¿Puede montar?", description: "User can mount external units", description_es: "El usuario podra montar unidades externas"}, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
  title_es: "Salvapantallas",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["idle_enabled", "lock_enabled"],
          order: ["lock_enabled", "lock_delay", "idle_enabled", "idle_delay"],
          properties: {
            idle_enabled: {
              type: "boolean",
              title: "Dim screen",
	          title_es: "Oscurecer pantalla"
            },
            idle_delay: {
              type: "string",
              description: "Time to dim screen in seconds",
              description_es: "Tiempo hasta el oscurecimiento en segundos",
              title: "Idle delay",
              title_es: "Retraso de inactividad"              
            },
            lock_enabled: {
              type: "boolean",
              title: "Allow screen lock",
              title_es: "Permitir bloqueo de pantalla"
            },
            lock_delay: {
              type: "string",
              description: "Time to lock the screen in seconds",
              description_es: " Tiempo hasta el bloqueo de la pantalla en segundos",
              title: "Time to lock",
              title_es: "Tiempo hasta el bloqueo"              
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
  title_es: "Permisos para compartir",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["can_share"],
          properties: {
            can_share: {title: "Can Share?", title_es: "¿Puede compartir?", description: "User can share folders", description_es: "El usuario tendrá permisos para compartir carpetas", type: "boolean"}, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
  title: "Control panel",
  title_es: "Panel de control",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["desktop_files"],
          properties: {
            desktop_files: {
              type: "array",
              title: "Categories",
              title_es: "Categorias",
              description: "Deletes the control panel category",
              description_es: "Elimina la categoría del panel de control",
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
    support_os: support_os_js.clone,
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
  title: "Application Menu",
  title_es: "Menú de aplicaciones",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario", 
          required: ["desktop_files_include", "desktop_files_exclude"],
          properties: {
            desktop_files_include: {
              type: "array",
              title: "Add application menu",
              title_es: "Añadir aplicación al menú",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "string"
              }
            },
            desktop_files_exclude: {
              type: "array",
              title: "Remove application menu",
              title_es: "Quitar aplicación del menú",
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
    support_os: support_os_js.clone,
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
  title_es: "Acceso directo en el escritorio",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["launchers"],
          properties: {
            launchers: {
              type: "array",
              title: "Shortcut",
              title_es: "Acceso directo",
              description: "Enter the name of a .desktop file describing the application", 
              description_es: "Introduzca el nombre del fichero .desktop que describe la aplicación",
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
    support_os: support_os_js.clone,
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
# title_es: "Fondo de escritorio",
#  type: "object",
#  required: ["desktop_file"],
#  properties: {
#    desktop_file: {type: "string", title: "Desktop File", title_es: "Archivo de escritorio"},
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
  title_es: "Fondo de escritorio",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["desktop_file"],
          properties: {
            desktop_file: {type: "string", title: "Image", title_es: "Imagen", description: "Fill with the absolute path to the image file", description_es: "Introduzca la ruta absoluta al archivo de imagen"},
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
  title_es: "Explorador de archivos",
  type: "object",
  required: ["users"],
  properties:{
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["default_folder_viewer", "show_hidden_files", "show_search_icon_toolbar", "click_policy", "confirm_trash"],
          order: ["click_policy", "show_hidden_files", "default_folder_viewer", "show_search_icon_toolbar", "confirm_trash"],
          properties: {
            default_folder_viewer: {type: "string", title: "files viewer", title_es: "Visualización de archivos", enum: ["icon-view", "compact-view", "list-view"], default: "icon-view"},
            show_hidden_files: {type: "string", title: "Show hidden files?", title_es: "Mostrar archivos ocultos", enum: ["true","false"], default: "false"},
            show_search_icon_toolbar: {type: "string", title: "Show search icon on toolbar?", title_es: "Mostrar el icono de búsqueda en la barra de herramientas", enum: ["true", "false"], default: "true"},
            confirm_trash: {type: "string", title: "Confirm trash?", title_es: "Confirmar al vaciar la papelera", enum: ["true","false"], default: "true"},
            click_policy: {type: "string", title: "Click policy", title_es: "Política de click", enum: ["single", "double"], default: "double"}, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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


cert_js = {
  title: "Certificate Management",
  title_es: "Gestion de Certificados",
  type: "object",
  properties:{
    java_keystores: {
      title: "Java Keystores",
      title_es: "Almacenes de claves de Java",
      description: "Path of java keystore: e.g. /etc/java/cacerts-gcj",
      description_es: "Ruta del almacén de claves: p.ej. /etc/java/cacerts-gcj",
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "string"
      }
    },
    ca_root_certs:{
      title: "CA root certificates",
      title_es: "Certificados raices de Autoridades de Certificación (CA)",
      type:"array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        properties:{
          name: {
            title: "Name",
            title_es: "Nombre",
            type: "string"
          },
          uri: {
            title: "Uri certificate",
            title_es: "Uri del certificado",
            type: "string"
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
  title_es: "Navegador Web",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      type: "object",
      title: "Users",
      title_es: "Usuarios",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          properties: {
            plugins: {
              type: "array",
              title: "Plugins",
              title_es: "Plugins", 
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["name", "uri", "action"],
                order: ["name", "uri", "action"],
                properties: {
                  name: {title: "Name", title_es: "Nombre", type: "string"},
                  uri: {title: "Uri", title_es: "Uri", type: "string"},
                  action: {title: "Action", title_es: "Acción", type: "string", enum: ["add", "remove"]}
                }
              }
            },
            bookmarks: {
              type: "array",
              title: "Bookmarks",
              title_es: "Marcadores",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["name", "uri"],
                order: ["name", "uri"],
                properties: {
                  name: {title: "Name", title_es: "Nombre", type: "string"},
                  uri: {title: "Uri", title_es: "Uri", type: "string"}
                }
              }
            },
            config: {
              type: "array",
              title: "Configs",
              title_es: "Configuraciones",
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["key"],
                order: ["key", "value_type", "value_str", "value_num", "value_bool"],
                properties: {
                  key: {type: "string", title: "Key", title_es: "Clave", description: "Enter a key to about:config", description_es: "Introduzca una clave de about:config"},
                  value_str: {type: "string",
                              description: "Only if Value Type is string",
                              description_es: "Solo si el tipo de valor es una cadena",
                              title: "Value",
                              title_es: "Valor"                              
                              },
                  value_num: {type: "number", 
                              description: "Only if Value Type is number",
                              description_es: "Solo si el tipo de valor es un numero",
                              title: "Value",
                              title_es: "Valor"                              
                              },
                  value_bool: {type: "boolean", 
                               description: "Only if Value Type is boolean",
                               description_es: "Solo si el tipo de valor es booleano",
                               title: "Value",
                               title_es: "Valor"                               
                               },
                  value_type: {title: "Value type", title_es: "Tipo de valor", type: "string", enum: ["string", "number", "boolean"]}

                }
              }
            #},
            #certs: {
            # type: "array",
            # title: "Certificates",
            # title_es: "Certificados",
            # minItems: 0,
            # uniqueItems: true,
            # items: {
            #   type: "object",
            #   required: [ "name", "uri"],
            #   properties: {
            #     name: {title: "Name", title_es: "Nombre", type: "string"},
            #     uri: {title: "Uri", 
            #           title_es: "Uri", 
            #           type: "string", 
            #           description: "Only accept CRT and PEM certificate", 
            #           description_es: "Solo acepta certificados CRT y PEM"}
            #   }
            # }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
email_client_js = {
  title: "Email Configuration",
  title_es: "Configuración de email",
  type: "object",
  properties: {
    users: {
      type: "object",
      title: "Users",
      title_es: "Usuarios",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["identity", "imap", "smtp"],
          order: ["identity", "imap", "smtp"],
          properties: {  
            identity: {
              title: "Identity of the user",
              title_es: "Identidad del usuario",
              type: "object",
              order: ["name", "email"],
              properties: {
                name: {
                  title: "Name",
                  title_es: "Nombre",
                  type: "string"
                },
                email: {
                  title: "Email address",
                  title_es: "Dirección de correo electrónico",
                  # pattern: TODO !!!!
                  type: "string"
                }
              }
            },
            imap: {
              title: "IMAP server",
              title_es: "Servidor IMAP",
              type: "object",
              order: ["username", "hostname", "port"],
              properties: {
                hostname: {
                  title: "Hostname",
                  title_es: "Hostname",
                  # pattern: TODO !!!!
                  type: "string"
                },
                port: {
                  title: "Port",
                  title_es: "Puerto",
                  default: 143,
                  # selector: 143 / Libre TODO !!!!
                  type: "number"
                },
                username: {
                  title: "Username",
                  title_es: "Nombre de usuario",
                  type: "string"
                }
              }
            },
            smtp: {
              title: "SMTP server",
              title_es: "Servidor SMTP",
              type: "object",
              order: ["username", "hostname", "port"],
              properties: {
                hostname: {
                  title: "Hostname",
                  title_es: "Hostname",
                  # pattern: TODO !!!!
                  type: "string"
                },
                port: {
                  title: "Port",
                  title_es: "Puerto",
                  default: 25,
                  # selector: 25 / 110 / Libre TODO !!!!
                  type: "number"
                },
                username: {
                  title: "Username",
                  title_es: "Nombre de usuario",
                  type: "string"
                }
              }
            },
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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

user_alerts_js = {
  title: "User alert",
  title_es: "Alertas de usuario",
  type: "object",
  properties: {
    users: {
      type: "object",
      title: "Users",
      title_es: "Usuarios",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["summary", "body"],
          order: ["summary", "body", "urgency", "icon"],
          properties: {  
            summary: {
              title: "Summary for the alert message",
              title_es: "Titulo para el mensaje de alerta",
              type: "string"
            }, 
            body: {
              title: "Body of the alert message",
              title_es: "Cuerpo del mensaje de alerta",
              type: "string"
            }, 
            urgency: {
              title: "Urgency level for the alert",
              title_es: "Nivel de urgencia de la alerta",
              type: "string",
              enum: ["low", "normal", "critical"],
              default: "normal"
            },
            icon: {
              title: "Icon filename or stock icon to display",
              title_es: "Fichero de icono o icono del stock a mostrar",
              description: "This policy will apply 5 minutes after synchronization",
              description_es: "Esta politica se aplicará 5 minutos después de la sincronización",
              type: "string",
              default: "info"
            },
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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

remote_shutdown_js = {
  title: "Remote shutdown",
  title_es: "Apagado remoto",
  type: "object",
  required: ["shutdown_mode"],
  properties: {
    shutdown_mode: {
      title: "Shutdown mode",
      title_es: "Tipo de apagado",
      description: "This policy will apply 5 minutes after synchronization",
      description_es: "Esta politica se aplicará 5 minutos después de la sincronización",
      type: "string",
      enum: ["halt", "reboot",""],
      default: "halt"
    }, 
    support_os: support_os_js.clone,
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
  title_es: "Carpetas Compartidas",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["gtkbookmarks"],
          properties: {
            gtkbookmarks: {
              type: "array",
              title: "Bookmarks",
              title_es: "Marcadores", 
              minItems: 0,
              uniqueItems: true,
              items: {
                type: "object",
                required: ["name", "uri"],
                properties: {
                  name: {title: "Name", title_es: "Nombre", type: "string"},
                  uri: {title: "Uri", title_es: "Uri", type: "string"}
                }
              }
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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
  title: "DEPRECATED: Applications Config",
  title_es: "OBSOLETA: Configuración de aplicaciones",
  type: "object",
 # required: ["citrix_config", "java_config", "firefox_config", "thunderbird_config", "loffice_config"],
  required: ["java_config", "loffice_config"],
  properties: {
    #citrix_config: {title: "Citrix Configuration", title_es: "Configuración de Citrix", type: "object"},
    java_config: {
      title: "Java Configuration",
      title_es: "Configuración de Java",
      type: "object",
      order: ["version", "plug_version", "sec", "crl", "warn_cert", "mix_code", "ocsp", "array_attrs"],
      properties: {
        version: {
          title: "Java Version",
          title_es: "Versión de Java",
          type: "string"
        },
        plug_version: {
          title: "Plugins Java version",
          title_es: "Plugins versión de Java",
          type: "string"
        },
        sec: {
          title: "Security Level",
          title_es: "Nivel de Seguridad",
          type: "string",
          enum: ["MEDIUM", "HIGH", "VERY_HIGH"],
          default: "MEDIUM"
        },
        crl: {
          title: "Use Certificate Revocation List",
          title_es: "Utilizar lista de revocación de certificados",
          type: "boolean",
          enum: [true,false],
          default: false
        },
        ocsp: {
          title: "Enable or disable Online Certificate Status Protocol",
          title_es: "Activar o desactivar el protocolo de estado de certificados en linea",
          type: "boolean",
          enum: [true,false],
          default: false
        },
        warn_cert: {
          title: "Show host-mismatch warning for certificate?",
          title_es: "¿Mostrar advertencia de incompatibilidad de host para el certificado?",
          type: "boolean",
          enum: [true,false],
          default: false
        },
        mix_code: {
          title: "Security verification of mix code",
          title_es: "Verificación de la seguridad de la combinación de código",
          type: "string",
          enum: ["ENABLE", "HIDE_RUN", "HIDE_CANCEL", "DISABLED"],
          default: "ENABLE"
        },
        array_attrs: {
          type: "array",
          minItems: 0,
          title: "Another configuration properties",
          title_es: "Otras propiedades de configuración",
          uniqueItems: true,
          items:{
            type: "object",
            required: ["key", "value"],
            properties: {
              key: {type: "string", title: "Key", title_es: "Clave"},
              value: {type: "string", title: "Value", title_es: "Valor"}
            }
          }
        }

      }
    },
    firefox_config: {
      title: "Firefox Configuration",
      title_es: "Configuración de Firefox",
      type: "object",
      properties: {
        app_update:{
          title: "Enable/Disable auto update",
          title_es: "Activar/Desactivar actualizaciones automáticas",
          type: "boolean",
          enum: [true,false],
          default: false
        }
      }
    },
    thunderbird_config: {
      title: "Thunderbird Configuration",
      title_es: "Configuración de Thunderbird",
      type: "object",
      properties: {
        app_update: {
          title: "Enable/Disable auto update",
          title_es: "Activar/Desactivar actualizaciones automáticas",
          type: "boolean",
          enum: [true,false],
          default: false
        }
      }
    },
    loffice_config: {
      title: "Libre Office Configuration",
      title_es: "Configuración de Libre Office",
      type: "object",
      properties: {
        app_update: {
          title: "Enable/Disable auto update",
          title_es: "Activar/Desactivar actualizaciones automáticas",
          type: "boolean",
          enum: [true,false],
          default: false
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

appconfig_libreoffice_js = {
  title: "LibreOffice Config",
  title_es: "Configuración de LibreOffice",
  type: "object",
  required: ["config_libreoffice"],
  properties: {
    config_libreoffice: {
      title: "LibreOffice Configuration",
      title_es: "Configuración de LibreOffice",
      type: "object",
      properties: {
        app_update: {
          title: "Enable/Disable auto update",
          title_es: "Activar/Desactivar actualizaciones automáticas",
          type: "boolean",
          enum: [true,false],
          default: false
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

appconfig_thunderbird_js = {
  title: "Thunderbird Config",
  title_es: "Configuración de Thunderbird",
  type: "object",
  required: ["config_thunderbird"],
  properties: {
    config_thunderbird: {
      title: "Thunderbird Configuration",
      title_es: "Configuración de Thunderbird",
      type: "object",
      properties: {
        app_update: {
          title: "Enable/Disable auto update",
          title_es: "Activar/Desactivar actualizaciones automáticas",
          type: "boolean",
          enum: [true,false],
          default: false
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

appconfig_firefox_js = {
  title: "Firefox Config",
  title_es: "Configuración de Firefox",
  type: "object",
  required: ["config_firefox"],
  properties: {
    config_firefox: {
      title: "Firefox Configuration",
      title_es: "Configuración de Firefox",
      type: "object",
      properties: {
        app_update: {
          title: "Enable/Disable auto update",
          title_es: "Activar/Desactivar actualizaciones automáticas",
          type: "boolean",
          enum: [true,false],
          default: false
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

appconfig_java_js = {
  title: "Java Config",
  title_es: "Configuración de Java",
  type: "object",
  required: ["config_java"],
  properties: {
   config_java: {
      title: "Java Configuration",
      title_es: "Configuración de Java",
      type: "object",
      order: ["version", "plug_version", "sec", "crl", "warn_cert", "mix_code", "ocsp", "array_attrs"],
      properties: {
        version: {
          title: "Java Version",
          title_es: "Versión de Java",
	  description: "Path to an installed Java version, example: /usr/lib/jvm/java-7-oracle",
	  description_es: "Path a una versión instalada de Java, ej.: /usr/lib/jvm/java-7-oracle",
          type: "string"
        },
        plug_version: {
          title: "Plugins Java version",
          title_es: "Plugins versión de Java",
	  description: "Path to an installed Java version, example: /usr/lib/jvm/java-7-oracle",
	  description_es: "Path a una versión instalada de Java, ej.: /usr/lib/jvm/java-7-oracle",
          type: "string"
        },
        sec: {
          title: "Security Level",
          title_es: "Nivel de Seguridad",
          type: "string",
          enum: ["MEDIUM", "HIGH", "VERY_HIGH"],
          default: "MEDIUM"
        },
        crl: {
          title: "Use Certificate Revocation List",
          title_es: "Utilizar lista de revocación de certificados",
          type: "boolean",
          enum: [true,false],
          default: false
        },
        ocsp: {
          title: "Enable or disable Online Certificate Status Protocol",
          title_es: "Activar o desactivar el protocolo de estado de certificados en linea",
          type: "boolean",
          enum: [true,false],
          default: false
        },
        warn_cert: {
          title: "Show host-mismatch warning for certificate?",
          title_es: "¿Mostrar advertencia de incompatibilidad de host para el certificado?",
          type: "boolean",
          enum: [true,false],
          default: false
        },
        mix_code: {
          title: "Security verification of mix code",
          title_es: "Verificación de la seguridad de la combinación de código",
          type: "string",
          enum: ["ENABLE", "HIDE_RUN", "HIDE_CANCEL", "DISABLED"],
          default: "ENABLE"
        },
        array_attrs: {
          type: "array",
          minItems: 0,
          title: "Another configuration properties",
          title_es: "Otras propiedades de configuración",
          uniqueItems: true,
          items:{
            type: "object",
            required: ["key", "value"],
            properties: {
              key: {type: "string", title: "Key", title_es: "Clave"},
              value: {type: "string", title: "Value", title_es: "Valor"}
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
          type: "string"
        }
    }, 
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

auto_updates_js = {
  title: "Automatic Updates Repository",
  title_es: "Actualizaciones automáticas de repositorios",
  type: "object",
  required: ["auto_updates_rules"],
  properties: {
    auto_updates_rules: {
      type: "object",
      title: "Auto Updates Rules",
      title_es: "Reglas de actualizaciones automáticas",
      required: ["onstop_update", "onstart_update", "days"],
      order: ["onstart_update", "onstop_update", "days"],
      properties: {
        onstop_update: {title: "Update on shutdown?", title_es: "Actualizar al apagado",  type: "boolean"},
        onstart_update: {title: "Update on start", title_es: "Actualizar al inicio", type: "boolean"},
        days: {
          type: "array",
          title: "Periodic dates",
          title_es: "Fechas periódicas",
          minItems: 0,
          uniqueItems: true,
          items: {
            type: "object",
            required: ["day", "hour", "minute"],
            order: ["day", "hour", "minute"],
            properties: {
              day: {
                title: "Day",
                title_es: "Día",
                type: "string",
                enum: ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
              },
              hour: {
                title: "Hour",
                title_es: "Hora",
                type: "integer",
                maximum: 23
              },
              minute: {
                title: "Minute",
                title_es: "Minuto",
                type: "integer",
                maximum: 59
              }

            }
          }
        },
        date: {
          title: "Specific Date",
          title_es: "Fecha específica",
          type: "object",
          order: ["month", "day", "hour", "minute"],
          properties: {
            day: {title: "Day", title_es: "Día", type: "string", pattern: "^([0-9]|[0-2][0-9]|3[0-1]|\\\*)$"},
            month: {title: "Month", title_es: "Mes", type: "string",pattern: "^(0?[1-9]|1[0-2]|\\\*)$"},
            hour: {title: "Hour", title_es: "Hora", type: "string", pattern: "^((([0-1][0-9])|[0-2][0-3])|\\\*)$"},
            minute: {title: "Minute", title_es: "Minuto", type: "string",pattern: "^([0-5][0-9]|\\\*)$"},
          }
        }
      }
    },
    support_os: support_os_js.clone,
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

user_modify_nm_js = {
  title: "Give network privileges to user",
  title_es: "Conceder permisos de red al usuario",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["can_modify"],
          properties: {
            can_modify: {
              title: "Can modify network?",
              title_es: "¿Permisos para modificar la red?",
              type: "boolean",
              enum: [true,false],
              default:true
            },
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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

user_apps_autostart_js = {
  title: "Applications that will run at the start of the system",
  title_es: "Aplicaciones que se ejecutarán al inicio",
  type: "object",
  required: ["users"],
  properties: {
    users: {
      title: "Users",
      title_es: "Usuarios",
      type: "object",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
        order: ["desktops", "desktops_to_remove"],        
          properties: {
              desktops: {
              title: "Applications",
              title_es: "Aplicaciones",
              description: ".desktop file must exist in /usr/share/applications",
              description_es: "Es necesario que exista el .desktop en /usr/share/applications",
              type: "array",
              minItems: 0,
              uniqueItems: true,
              items: {type: "string"}
              },
              desktops_to_remove: {
              title: "Applications to remove from autostart",
              title_es: "Aplicaciones a eliminar del inicio",
              description: "Applications will not be run at session start anymore",
              description_es: "Las aplicaciones ya no se ejecutarán al inicio de sesión",
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
    support_os: support_os_js.clone,
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
  title: "Administration Date/Time",
  title_es: "Administración fecha/hora",
  type: "object",
  required: ["server"],
  properties: {
    server: {
      type: "string",
      title: "Server NTP",
      title_es: "Servidor NTP",
      description: "Enter the URI of an NTP server",
      description_es: "Introduzca la URI de un servidor NTP"
    },
    support_os: support_os_js.clone,
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
  title_es: "Lanzador de scripts",
  type: "object",
  required: ["on_startup","on_shutdown"],
  order: ["on_startup", "on_shutdown"],
  properties:
  {
    on_startup: {
      type: "array",
      title: "Script to run on startup",
      title_es: "Script para ejecutar al inicio",
      description: "Enter the absolute path to the script",
      description_es: "Introduzca la ruta absoluta al script",
      minItems: 0,
      uniqueItems: false,
      items: {
        type: "string",
        }
    },
    on_shutdown: {
      type: "array",
      title: "Script to run on shutdown",
      title_es: "Script para ejecutar al apagado",
      description: "Enter the absolute path to the script",
      description_es: "Introduzca la ruta absoluta al script",
      minItems: 0,
      uniqueItems: false,
      items: {
        type: "string",
        }
    },
    support_os: support_os_js.clone,
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
  type: "object",
  title: "Network Manager",
  title_es: "Administrador de red",
  required: ["connections"],
  properties:
  {
    connections: {
      type: "array",
      minItems: 0,
      uniqueItems: true,
      items: {
        type: "object",
        required: ["name", "mac_address", "use_dhcp", "net_type"],
        properties: {
          fixed_con: {
            title: "DHCP Disabled properties", 
            title_es: "Propiedades desactivadas de DHCP",
            description: "Only if DHCP is disabled",
            description_es: "Solo si el DHCP esta desactivado",
            type: "object",
            properties:{
              addresses: {
                type: "array",
                uniqueItems: true,
                minItems: 0,
                description: "This field is only used if DHCP is disabled",
                description_es: "Este campo solo se usará si el DHCP está desactivado",
                title: "IP addresses",
                title_es: "Dirección IP",
                items: {
                  type: "object",
                  #required: [ "ip_addr","netmask"],
                  properties:{
                    ip_addr: {
                      type: "string",
                      title: "IP address",
                      title_es: "Dirección IP",
                      description: "ipv4 format",
                      description_es: "Formato IPV4",
                      format: "ipv4"
                    },
                    netmask: {
                      type: "string",
                      title: "Netmask",
                      title_es: "Máscara de red",
                      description: "ipv4 format",
                      description_es: "Formato IPV4",
                      format: "ipv4"
                    }
                  }
                } 
              },
              gateway: {
                type: "string",
                title: "Gateway",
                title_es: "Puerta de enlace",
                description: "ipv4 format",
                description_es: "Formato ipv4",
                format: "ipv4"
              },
              dns_servers: {
                type: "array",
                title: "DNS Servers",
                title_es: "Servidor DNS",
                description: "With DHCP disable",
                description_es: "Con DHCP desactivado",
                minItems: 0,
                uniqueItems: true,
                items: {
                  type: "string",
                  title: "DNS",
                  title_es: "DNS",
                  description: "ipv4 format",
                  description_es: "Formato ipv4",
                  format: "ipv4"
                }
              }
            }
          },
          name: {type: "string", title: "Network name", title_es: "Nombre de la red"},
          mac_address: {pattern: "^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$", type: "string", title: "MAC address", title_es: "Dirección MAC"},
          use_dhcp: {type: "boolean", enum: [true,false], default:true, title: "DHCP", title_es: "DHCP"},
          net_type:{
            enum: ["wired", "wireless"], title: "Connection type", title_es: "Tipo de conexión", type: "string"
          },
          wireless_conn:{
            type:"object",
            title: "Wireless Configuration",
            title_es: "Configuración Wireless",
            properties:{
              essid: { type: "string", title: "ESSID", title_es: "ESSID" },
              security: { 
                type: "object", 
                title: "Security Configuration",
                title_es: "Configuración de Seguridad",
                required: ["sec_type"],
                order: ["sec_type", "auth_type", "enc_pass", "auth_user", "auth_password"],
                properties:{
                  sec_type: { enum: [ "none", "WEP", "Leap", "WPA_PSK"], default:"none", title: "Security type", title_es: "Tipo de seguridad", type:"string"},
                  enc_pass: { type: "string", 
                              description: "WEP, WPA_PSK security",
                              description_es: "WEP, seguridad WPA_PSK ",
                              title: "Password",
                              title_es: "Contraseña"                   
                            },
                  auth_type: { enum: ["OpenSystem", "SharedKey"], 
                               title: "Authentication type",
                               title_es: "Tipo de autenticación",
                               description: "WEP security",
                               description_es: "Seguridad WEP",
                               type: "string", 
                               default: "OpenSystem"},
                  auth_user: { type: "string",
                               description: "Leap security",
                               description_es: "Seguridad Leap",
                               title: "Username",
                               title_es: "Nombre de usuario"                                
                               },
                  auth_password: { type: "string",
                                   description: "Leap security",
                                   description_es: "Seguridad Leap",
                                   title: "Password",
                                   title_es: "Contraseña"
                                 }

                }
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
        type: "string"
      }
    }, 
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

software_sources_js = {
  title: "Software Sources",
  title_es: "Fuentes de software",
  type: "object",
  required: ["repo_list"],
  properties:{
    repo_list: {
      type:"array",
      items: {
        type:"object",
        required: ["repo_name","uri","deb_src","repo_key","key_server"],
        properties:{
          components: { title: "Components", title_es: "Componentes", type: "array",items: { type: "string" } },
          deb_src: { title: "Sources", title_es: "Fuentes", type: "boolean", default: false },
          repo_key: { title: "Repository key", title_es: "Clave del repositorio", type: "string", default: ""},
          key_server: { title: "Server key", title_es: "Clave del servidor", type: "string", default: ""},
          distribution: { title: "Distribution", title_es: "Distribución", type: "string"},
          repo_name: { title: "Repository name", title_es: "Nombre del repositorio", type: "string"},
          uri: { title: "Uri", title_es: "Uri", type: "string" }
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
    support_os: support_os_js.clone,
    updated_by: updated_js
   }
}

package_profile_js = {
  title: "Packages Profile management",
  title_es: "Administración de perfiles de software",
  type: "object",
  order:["package_list"],
  properties:
  {
    package_list: {
      type:"array",
      title: "Package list to install",
      title_es: "Lista de paquetes para instalar",
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

package_js = {
  title: "Packages management",
  title_es: "Administración de paquetes",
  type: "object",
  order:["package_list", "pkgs_to_remove"],
  properties:
  {
    package_list: {
      type:"array",
      title: "Package list to install",
      title_es: "Lista de paquetes para instalar",
      minItems: 0,
      uniqueItems: true,
      items: {type: "string"}
    },
    pkgs_to_remove: {
      type:"array",
      title: "Package list to remove",
      title_es: "Lista de paquetes para eliminar",
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

printers_js = {
  title: "Printers",
  title_es: "Impresoras",
  type: "object",
  required: ["printers_list"],
  properties:
  {
    printers_list: {
      type:"array",
      title: "Printer list to enable",
      title_es: "Lista de impresoras para activar",
      items: {
        type:"object",
        required: [ "name", "manufacturer", "model", "uri"],
        properties:{
          name: { type: "string", title: "Name", title_es: "Nombre"},
          manufacturer: { type: "string", title: "Manufacturer", title_es: "Manufactura" },
          model: { type: "string" , title: "Model", title_es: "Modelo"},
          uri: { type: "string", title: "Uri", title_es: "Uri"},
          ppd_uri: { type: "string", title: "Uri PPD", title_es: "Uri PPD", default: "", pattern: "(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"},
          ppd: { type: "string", title: "PPD Name", title_es: "Nombre PPD"},
          oppolicy: {enum: ["default","authenticated"], default:"default", type: "string", title: "Operation Policy", title_es: "Politica de Autenticación"}
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
    support_os: support_os_js.clone,
    updated_by: updated_js
  }
}

local_users_js = {
  title: "Users",
  title_es: "Usuarios",
  type: "object",
  required: ["users_list"],
  properties:
  {users_list: {
      type:"array",
      title: "User list to manage",
      title_es: "Lista de usuarios para gestionar",
      items: {
        type:"object",
        required: ["user","actiontorun"],
        order:["actiontorun", "user", "password", "name", "groups"],
        properties:{
          actiontorun: {enum: ["create","modify","delete"],type: "string", title: "Action", title_es: "Acción"},
          groups: { title: "Groups", title_es: "Grupos", type: "array",items: { type: "string" } },
          user: { title: "User", title_es: "Usuario", type: "string" },
          name: { title: "Full Name", title_es: "Nombre Completo", type: "string" },
          password: { title: "Password", title_es: "Contraseña", type: "string"}
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
  support_os: support_os_js.clone,
  updated_by: updated_js
 }
}

local_groups_js = {
  title: "Local groups",
  title_es: "Grupos locales",
  type: "object",
  required: ["groups_list"],
  properties:
  {groups_list: {
      type:"array",
      title: "Group to manage",
      title_es: "Grupos para gestionar",
      items: {
        type:"object",
        required: ["group","users","remove_users","create"],
        order:["users", "group", "remove_users", "create"],
        properties:{
          group: { type: "string", title: "Group", title_es: "Grupo" },
          users: { type: "array",title: "Users", title_es: "Usuarios", items: { type: "string" } },
          remove_users: { type: "boolean", title: "Remove users", title_es: "Eliminar usuarios", description: "Remove users in list", description_es: "Eliminar los usuarios de la lista", default: false },
          create: { type: "boolean", title: "Create group", title_es: "Crear grupo", description: "Create group if it doesn't exist in node", description_es: "Crear grupo si no existe", default: false } 
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
  support_os: support_os_js.clone,
  updated_by: updated_js
 }
}

local_file_js = {
  title: "Local files",
  title_es: "Archivos locales",
  type: "object",
  required: ["delete_files", "copy_files"],
  order: ["copy_files", "delete_files"],
  properties:
  {delete_files: {
      type:"array",
      title: "File list to delete",
      title_es: "Lista de archivos para eliminar",
      items: {
        type:"object",
        required: ["file"],
        order:["file", "backup"],
        properties:{
          file: {type: "string", title:"File", title_es: "Archivo", description: "Enter the absolute path of the file to delete", description_es: "Introduzca la ruta absoluta del archivo a borrar"},
          backup: { type: "boolean", title: "Create backup?", title_es: "¿Crear copia de seguridad?" }
        }
     }
  },
  copy_files: {
    type: "array",
    title: "File list to copy",
    title_es: "Lista de archivos para copiar",
    items: {
      type: "object",
      required: ["file_orig","file_dest"],
      order:["user", "group", "file_orig", "file_dest", "mode", "overwrite"],
      properties:{
        file_orig: {type: "string", title: "File URL", title_es: "URL del archivo", description: "Enter the URL where the file was downloaded", description_es: "Introduzca la URL donde se descargará el archivo"},
        file_dest: {type: "string", title: "File Path", title_es: "Ruta del archivo", description: "Enter the absolute path where the file is saved", description_es: "Introduzca la ruta absoluta donde se guardará el archivo"},
        user: {type: "string", title:"User", title_es: "Usuario"},
        group: {type: "string", title: "Group", title_es: "Grupo"},
        mode: {type: "string", title: "Mode", title_es: "Permisos"},
        overwrite: {type: "boolean", title: "Overwrite?", title_es: "Sobrescribir"}
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
  support_os: support_os_js.clone,
  updated_by: updated_js
 }
}

local_admin_users_js = {
  title: "Local Administrators",
  title_es: "Administradores locales",
  type: "object",
  required: ["local_admin_list"],
  order: ["local_admin_list", "local_admin_remove_list"],
  properties:
  {local_admin_list: {
      type:"array",
      title: "users",
      title_es: "Usuarios", 
      description: "Enter a local user to grant administrator rights",
      description_es: "Escriba un usuario local para concederle permisos de administrador",
      items: { type:"string"}
  },
local_admin_remove_list: {
      type:"array",
      title: "users_to_remove",
      title_es: "Usuarios a eliminar", 
      description: "Enter a local user to revoke administrator rights",
      description_es: "Escriba un usuario local para eliminar sus permisos de administrador",
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
  support_os: support_os_js.clone,
  updated_by: updated_js
 }
}

folder_sync_js = {
  title: "Folder to sync",
  title_es: "Carpeta para sincronizar",
  type: "object",
  required: ["users"],
  properties:
  {users: {
    title: "Users", 
    title_es: "Usuarios",
    type: "object",
    patternProperties: {
      ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
        properties: {
          owncloud_url: {title: "Owncloud URL", title_es: "URL de Owncloud", type: "string"},
          updated_by: updated_js
        }
      }
    }
  },
  support_os: support_os_js.clone,
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
  title_es: "Administración de energía",
  type: "object",
#  required: ["cpu_freq_gov","auto_shutdown","usb_autosuspend"],
  order: ["cpu_freq_gov", "usb_autosuspend", "auto_shutdown"],
  properties:
    {cpu_freq_gov: {
       title: "CPU frequency governor",
       title_es: "Control de la frecuencia de la CPU", 
       type: "string",
       enum: ["userspace","powersave","conservative","ondemand","performance",""]
       },
    usb_autosuspend: 
      {
       title: "USB autosuspend",
       title_es: "Suspensión automática de USB",
       type: "string",  
       enum: ["enable","disable", ""]
       },
     auto_shutdown: {
       type: "object",
       order: ["hour", "minute"],
       properties: {
         hour: {
           title: "Hour",
           title_es: "Hora",
           description:"Time when the computer is shutdown",
           description_es: "Hora en que se apagará el equipo",
           type: "integer",
           maximum: 23
           },
         minute: {
           title: "Minute",
           title_es: "Minuto",
           description:"Minute the computer will shutdown",
           description_es: "Minuto en que se apagará el equipo",
           type: "integer",
           maximum: 59
         }
       }  
  },
  support_os: support_os_js.clone,
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
  title_es: "Opciones de apagado",
  type: "object",
  required: ["users"],
  properties: { 
    systemlock: { type: "boolean", title: "System-wide lockdown of the key", title_es: "Bloqueo para todo el sistema de la llave"},
    users: {
      type: "object", 
      title: "Users",
      title_es: "Usuarios",
      patternProperties: {
        ".*" => { type: "object", title: "Username", title_es: "Nombre de usuario",
          required: ["disable_log_out"],
          properties:{
            disable_log_out: {
              title: "Disable log out?",
              title_es: "¿Desactivar apagado?",
              description: "Checking the box will not allow the computer turns off",
              description_es: "Si activa la casilla no permitira el apagado del equipo",
              type: "boolean",
              default: false
            }, 
            updated_by: updated_js
          }
        }
      }
    },
    support_os: support_os_js.clone,
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

network_resource_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
tz_date_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
scripts_launch_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
local_users_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
local_file_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
auto_updates_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
local_groups_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
power_conf_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
local_admin_users_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
software_sources_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
package_js[:properties][:support_os][:default]=["GECOS V2","Ubuntu 14.04.1 LTS","Gecos V2 Lite"]
package_profile_js[:properties][:support_os][:default]=["GECOS V2","Ubuntu 14.04.1 LTS","Gecos V2 Lite"]
app_config_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
appconfig_libreoffice_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
appconfig_thunderbird_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
appconfig_firefox_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
appconfig_java_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
printers_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
user_shared_folders_js[:properties][:support_os][:default]=["GECOS V2"]
web_browser_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
email_client_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
file_browser_js[:properties][:support_os][:default]=["GECOS V2"]
user_launchers_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
desktop_background_js[:properties][:support_os][:default]=["GECOS V2"]
desktop_menu_js[:properties][:support_os][:default]=[]
desktop_control_js[:properties][:support_os][:default]=[]
user_apps_autostart_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
folder_sharing_js[:properties][:support_os][:default]=["GECOS V2"]
screensaver_js[:properties][:support_os][:default]=["GECOS V2"]
folder_sync_js[:properties][:support_os][:default]=["GECOS V2"]
user_mount_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
user_alerts_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
remote_shutdown_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
forticlientvpn_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
user_modify_nm_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
shutdown_options_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
cert_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]
mobile_broadband_js[:properties][:support_os][:default]=["GECOS V2","Gecos V2 Lite"]

complete_js = {
  description: "GECOS workstation management LWRPs json-schema",
  description_es: "Estación de trabajo de gestión GECOS LWRPs json-schema",
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
          required: ["network_res","forticlientvpn_res","mobile_broadband_res"],
          properties: {
            network_res: network_resource_js,
            forticlientvpn_res: forticlientvpn_js,
            mobile_broadband_res: mobile_broadband_js
            #sssd_res: sssd_js
          }
        },
        misc_mgmt: {
          type: "object",
          required: ["tz_date_res", "scripts_launch_res", "local_users_res", "local_groups_res", "local_file_res", "local_admin_users_res", "auto_updates_res","power_conf_res","remote_shutdown_res","cert_res"],
          properties: {
            tz_date_res: tz_date_js,
            scripts_launch_res: scripts_launch_js,
            local_users_res: local_users_js,
            local_file_res: local_file_js,
           # desktop_background_res: desktop_background_js,
            auto_updates_res: auto_updates_js,
            local_groups_res: local_groups_js,
            power_conf_res: power_conf_js,
            local_admin_users_res: local_admin_users_js,
            remote_shutdown_res: remote_shutdown_js,
            cert_res: cert_js
          }
        },
        software_mgmt: {
          type: "object",
          required: ["software_sources_res","package_res", "app_config_res","appconfig_libreoffice_res","appconfig_thunderbird_res","appconfig_firefox_res","appconfig_java_res","package_profile_res"],
          properties: {
            software_sources_res: software_sources_js,
            package_res: package_js,
            package_profile_res: package_profile_js,
            app_config_res: app_config_js,
	    appconfig_libreoffice_res: appconfig_libreoffice_js,
            appconfig_thunderbird_res: appconfig_thunderbird_js,
	    appconfig_firefox_res: appconfig_firefox_js,
	    appconfig_java_res: appconfig_java_js
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
          required: ["user_apps_autostart_res", "user_shared_folders_res", "web_browser_res", "email_client_res", "file_browser_res", "user_launchers_res", "desktop_menu_res", "desktop_control_res", "folder_sharing_res", "screensaver_res","folder_sync_res", "user_mount_res","shutdown_options_res","desktop_background_res","user_alerts_res"],
          properties: {
            user_shared_folders_res: user_shared_folders_js,
            web_browser_res: web_browser_js,
            email_client_res: email_client_js,
            file_browser_res: file_browser_js,
            user_alerts_res: user_alerts_js,
            user_launchers_res: user_launchers_js,
            desktop_background_res: desktop_background_js,
            desktop_menu_res: desktop_menu_js,
            desktop_control_res: desktop_control_js,
            user_apps_autostart_res: user_apps_autostart_js,
            folder_sharing_res: folder_sharing_js,
            screensaver_res: screensaver_js,
            folder_sync_res: folder_sync_js,
            user_mount_res: user_mount_js,
            user_modify_nm_res: user_modify_nm_js,
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
