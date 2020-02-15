import casatools as ctl
import casatasks as ctk

logfile=ctk.casalog.logfile()
os.system('rm -rf '+logfile+' '+'test_casa6.log')
ctk.casalog.setlogfile('logs/test_casa6.log')
ctk.casalog.showconsole(onconsole=True)