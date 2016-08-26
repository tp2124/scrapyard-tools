import sy_lib_perforce as P4

p4 = P4.P4(client='primm_desktop_scrapyard')
p4.connected()
p4.p4Info(True)
