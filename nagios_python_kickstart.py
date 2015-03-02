import shlex, sys
from optparse import OptionParser
from subprocess import Popen, PIPE, STDOUT

def main():
	# The following allows this script to accept command line arguments
	# for warning and critical thresholds. Add other options as you see fit.
	# Note: optparse is used instead of argparse for backwards compatability
	# with Python versions back to 2.4.
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option("-w", "--warning",
	                  action="store", type="int", dest="warning",
	                  help="warning threshold")
	parser.add_option("-c", "--critical",
	                  action="store", type="int", dest="critical",
	                  help="critical threshold")
	(options, args) = parser.parse_args()
	# Execute the plugin check logic.
	check_execution = perform_check()
	# Evaluate the results of the check execution against the thresholds.
	process_results(check_execution, 
					int(options.warning), int(options.critical))


def perform_check():
	# Assign commands to be performed to the command# variable below
	# as a string. Note that commands piped into other commands have to
	# be defined as separate processes / commands.
	# 	bash example: "ls -l '/tmp' | wc -l"
	command1 = "/bin/ls -l '/tmp'"
	command2 = "wc -l"
	command_args1 = shlex.split(command1)
	command_args2 = shlex.split(command2)
	# Execute the commands and merge stderr and stdout streams
	process1 = Popen(command_args1,
							stdout=PIPE, stderr=STDOUT)
	process2 = Popen(command_args2, stdin=process1.stdout,
							stdout=PIPE, stderr=STDOUT)
	output, err = process2.communicate()
	process_return_code = process2.returncode
	# Return a dictionary that contains the result and return code of the
	# command execution.
	check_execution = {'result': output, 'return_code': process_return_code}
	return check_execution


def process_results(check_execution, warning, critical):
	# Evaluate the result of the command execution against the 
	# threshold values supplied on the command line.
	# Change the evaluation logic to match your specific needs.

	# Specify a unit of measure for the metric to be used in the graph.
	# Metrics should conform to the units of measure supported by
	# pnp4nagios: no unit specified; s; %; B(KB,MB,GB,TB); c.
	uom=''
	# Specify a name for the metric to be displayed on the graph.
	metric_name='number of files'
	# Exit with Nagios' UNKNOWN status code if 
	# check_execution's return code is non-zero.
	if check_execution['return_code'] != 0:
		print "An unknown error occured: %s | " % (check_execution['result'])
		sys.exit(3)
	# Exit with CRITICAL status code if CRITICAL threshold is exceeded.
	# Display Nagios performance data in format expected by pnp4nagios.
	if int(check_execution['result']) > critical:
		print "CRITICAL - Check exceeds threshold. %s=%d | '%s'=%d%s;%d;%d;;" % \
			(metric_name, int(check_execution['result']), metric_name, 
			int(check_execution['result']), uom, warning, critical)
		sys.exit(2)
	# Exit with WARNING status code if WARNING threshold is exceeded.
	# Display Nagios performance data in format expected by pnp4nagios.
	elif int(check_execution['result']) > warning:
		print "WARNING - Check exceeds threshold. %s=%d | '%s'=%d%s;%d;%d;;" % \
			(metric_name, int(check_execution['result']), metric_name, 
			int(check_execution['result']), uom, warning, critical)
		sys.exit(1)
	else:
	# Exit with OK status code if results are within accpetable range.
	# Display Nagios performance data in format expected by pnp4nagios.
		print "OK. %s=%d | '%s'=%d%s;%d;%d;;" % \
			(metric_name, int(check_execution['result']), metric_name, 
			int(check_execution['result']), uom, warning, critical)
		sys.exit(0)


if __name__ == '__main__':
	main()