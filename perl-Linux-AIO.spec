#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Linux
%define	pnam	AIO
Summary:	Linux::AIO - linux-specific aio implemented using clone
#Summary(pl):	-
Name:		perl-%{pdir}-%{pnam}
Version:	1.3
Release:	1
License:	Unknown
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	e2f2b749d384d948e813fa2979ade315
URL:		http://search.cpan.org/dist/Linux-AIO/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements asynchronous i/o using the means available to
linux - clone. It does not hook into the POSIX aio_* functions because
linux does not yet support these in the kernel (and even if, it would
only allow aio_read and write, not open and stat).

Instead, in this module a number of (non-posix) threads are started
that execute your read/writes and signal their completion. You don't
need thread support in your libc or perl, and the threads created by
this module will not be visible to the pthreads library.

NOTICE: the threads created by this module will automatically be
killed when the thread calling min_parallel exits. Make sure you only
ever call min_parallel from the same thread that loaded this module.

Although the module will work with threads, it is not reentrant, so
use appropriate locking yourself.

#%description -l pl

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/Linux/*.pm
%{_mandir}/man3/*
