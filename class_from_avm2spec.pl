sub fix_name {
	$type = @_[0];

	$type =~ s/'//g;
	$newtype = '';
	foreach $_ (split (/_/, $type)) {
		s/(\w)(.*)/uc($1).$2/eg;
		$newtype .= $_;
	}

	return $newtype;
}

my $actionscript_ints = 1;

my @lines = ();

my $classname = <>;
$classname =~ s/\s$//;
$classname = fix_name ($classname);

$_ = <>;

while (<>) {
	s/^\s*(.*)\s*$/\1/;

	s/ /', '/;
	s/\[(\w+)\]/', '\1/;
	s/^(.*[^,])$/\1'/;
	s/^/'/;

	($type, $name, $arraylen) = split /\s*,\s*/;

	$name =~ s/\s//g;

	if (!$name) {
		next;
	}

	if ($type =~ /^[a-zA-Z_']+$/) {
		$type = fix_name ($type);
	} else {
		if ($actionscript_ints)  {
			$type =~ s/s32/vls32/;
			$type =~ s/u32/vlu32/;
		} else {
			$type =~ s/s32/i/;
			$type =~ s/u32/I/;
		}

		$type =~ s/u8/B/;
		$type =~ s/u16/H/;
		$type =~ s/s16/h/;
		$type =~ s/d64/d/;
		$type =~ s/u30/vlu30/;
	}

	if ($arraylen) {
		push @lines, "($type, $name, $arraylen),";
	} else {
		push @lines, "($type, $name),";
	}
}

print "class $classname (AVM2Unpackable):\n";
print "\t_struct = [\n";

foreach (@lines) {
	print "\t\t$_\n";
}

print "\t]";
print "\n";