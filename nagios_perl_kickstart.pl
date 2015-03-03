#!/usr/bin/env perl
use strict;
use warnings;

use Getopt::Long;
my ($warning, $critical);
GetOptions (	"warning|w=i" 	=> \$warning,
				"critical|c=i"	=> \$critical)
or die("Error in command line arguments\n");

my $check_execution = `/usr/bin/ls -l "/tmp" | wc -l`;
my $execution_return_code = $? >> 8;