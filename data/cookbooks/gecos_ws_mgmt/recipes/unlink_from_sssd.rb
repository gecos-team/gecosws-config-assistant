gecos_ws_mgmt_sssd 'deconfigure_sssd' do
  domain node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:domain]
  enabled node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled]
  job_ids []
  support_os node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:support_os]
  action  :setup
end
